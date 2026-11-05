"""Bounded logical backups; restore only to new, isolated recovery targets."""

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile

from sqlalchemy import DateTime, func, insert, select

from app.db import Base

FORMAT = "chef-logical-backup-1"
MAX_BYTES = 128 * 1024 * 1024
MAX_FILES = 2000


def encode(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError("Unsupported snapshot value")


def json_bytes(value):
    return json.dumps(value, default=encode, ensure_ascii=False, allow_nan=False).encode("utf-8")


def manifest_for(files, counts, constitution_digest):
    return {
        "format": FORMAT,
        "schema_revision": "0003",
        "created_at": datetime.now(UTC).isoformat(),
        "constitution_digest": constitution_digest,
        "row_counts": counts,
        "files": {
            name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in files.items()
        },
        "scope": "All application owners, source revisions, indexes, audit, cooking records and push subscriptions; Markdown Vault only. Includes private push subscription keys, excludes API tokens and server private keys.",
    }


def snapshot_database(engine):
    tables, counts = {}, {}
    with engine.connect() as connection:
        if engine.dialect.name == "postgresql":
            connection = connection.execution_options(isolation_level="REPEATABLE READ")
        with connection.begin():
            total = 0
            for table in Base.metadata.sorted_tables:
                rows = [
                    dict(row)
                    for row in connection.execute(
                        select(table).order_by(*table.primary_key.columns).limit(100_001 - total)
                    ).mappings()
                ]
                total += len(rows)
                if total > 100_000:
                    raise ValueError("Logical snapshot row limit exceeded; use pg_dump")
                tables[table.name], counts[table.name] = rows, len(rows)
    data = json_bytes(tables)
    if len(data) > MAX_BYTES // 2:
        raise ValueError("Logical database size limit exceeded; use pg_dump")
    return data, counts


def snapshot_vault(root):
    root = Path(root).resolve(strict=True)
    files = {}
    for path in sorted(root.rglob("*.md")):
        if not path.resolve().is_relative_to(root) or path.is_symlink():
            raise ValueError("Vault links outside snapshot boundaries are not allowed")
        before = path.stat()
        if before.st_size > 262_144:
            raise ValueError("Vault Markdown exceeds 256 KiB")
        data = path.read_bytes()
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError("Vault changed during snapshot; retry when edits are paused")
        files["vault/" + path.relative_to(root).as_posix()] = data
        if len(files) > MAX_FILES - 2 or sum(map(len, files.values())) > MAX_BYTES // 2:
            raise ValueError("Vault snapshot limit exceeded")
    return files


def create_backup(engine, vault_root, output, constitution_path):
    output = Path(output)
    data, counts = snapshot_database(engine)
    files = snapshot_vault(vault_root)
    files["database.json"] = data
    files["constitution.md"] = Path(constitution_path).read_bytes()
    if sum(map(len, files.values())) > MAX_BYTES - 1_048_576:
        raise ValueError("Combined archive exceeds snapshot limit")
    manifest = manifest_for(files, counts, hashlib.sha256(files["constitution.md"]).hexdigest())
    # Exclusive creation preserves existing backups. On write failure retain partial file for inspection.
    with output.open("xb") as stream, ZipFile(stream, "w", ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
        archive.writestr("manifest.json", json_bytes(manifest))
    return manifest


def read_backup(path):
    with ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES + 1 or sum(i.file_size for i in infos) > MAX_BYTES:
            raise ValueError("Backup exceeds restore limits")
        names = [i.filename for i in infos]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive entries")
        for name in names:
            parts = PurePosixPath(name)
            if parts.is_absolute() or ".." in parts.parts or "\\" in name or ":" in name:
                raise ValueError("Unsafe archive path")
            if name not in {"database.json", "constitution.md", "manifest.json"} and (
                not name.startswith("vault/") or not name.endswith(".md")
            ):
                raise ValueError("Unexpected backup file")
        manifest = json.loads(archive.read("manifest.json"))
        if manifest.get("format") != FORMAT or manifest.get("schema_revision") not in {"0001", "0002", "0003"}:
            raise ValueError("Unsupported backup format/schema")
        if set(names) != set(manifest["files"]) | {"manifest.json"}:
            raise ValueError("Manifest does not match archive")
        files = {}
        for name, expected in manifest["files"].items():
            data = archive.read(name)
            if len(data) != expected["size"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                raise ValueError("Backup checksum mismatch")
            files[name] = data
    if hashlib.sha256(files["constitution.md"]).hexdigest() != manifest["constitution_digest"]:
        raise ValueError("Constitution checksum mismatch")
    return manifest, files


def restore_backup(engine, archive_path, vault_target):
    database = engine.url.database or ""
    if engine.dialect.name == "postgresql":
        if not database.endswith(("_restore", "_test")):
            raise ValueError("Restore database name must end in _restore or _test")
    elif engine.dialect.name == "sqlite":
        if not Path(database).name.endswith("_restore.sqlite"):
            raise ValueError("SQLite restore filename must end in _restore.sqlite")
    else:
        raise ValueError("Unsupported restore database")
    target = Path(vault_target).absolute()
    if target.exists() or not target.parent.is_dir() or not target.name.endswith("_restore"):
        raise ValueError(
            "Vault target must be a nonexistent directory ending in _restore with an existing parent"
        )
    manifest, files = read_backup(archive_path)
    tables = json.loads(files["database.json"])
    if manifest["schema_revision"] == "0001" and "culinary_source_revisions" not in tables:
        tables["culinary_source_revisions"] = []
        manifest["row_counts"]["culinary_source_revisions"] = 0
    if manifest["schema_revision"] in {"0001", "0002"}:
        for name in ("action_log_sessions", "action_log_entries", "action_log_mutations", "web_push_subscriptions", "web_push_deliveries"):
            tables[name] = []
            manifest["row_counts"][name] = 0
    if set(tables) != set(Base.metadata.tables):
        raise ValueError("Snapshot table set does not match application schema")
    with engine.begin() as connection:
        # Target schema must already be migrated. Never create/drop/reset tables here.
        for table in Base.metadata.sorted_tables:
            if connection.scalar(select(func.count()).select_from(table)):
                raise ValueError("Refusing to restore into a nonempty database")
        for table in Base.metadata.sorted_tables:
            rows = tables[table.name]
            if len(rows) != manifest["row_counts"][table.name]:
                raise ValueError("Row count mismatch")
            for row in rows:
                if set(row) != set(table.c.keys()):
                    raise ValueError("Snapshot columns do not match schema")
                for column in table.c:
                    if isinstance(column.type, DateTime) and row[column.name] is not None:
                        row[column.name] = datetime.fromisoformat(row[column.name])
            if rows:
                connection.execute(insert(table), rows)
        # Never extract archive paths blindly. Preserve partial recovery files on failure.
        target.mkdir()
        for name, data in files.items():
            if name.startswith("vault/"):
                destination = target / name.removeprefix("vault/")
                if not destination.resolve().is_relative_to(target.resolve()):
                    raise ValueError("Restore destination escaped target")
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("xb") as stream:
                    stream.write(data)
    return {"status": "restored", "row_counts": manifest["row_counts"], "vault_target": str(target)}
