import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from app.backup import create_backup, read_backup, restore_backup
from app.chef import respond
from app.db import Base, make_engine, session_factory
from app.schemas import ChefRequest
from conftest import approve, chef_body, import_doc

CONSTITUTION = Path(__file__).resolve().parents[1] / "docs" / "CHEF_CONSTITUTION_0_1.md"


def snapshot(env, tmp_path):
    target = tmp_path / "snapshot.zip"
    create_backup(env["engine"], env["root"], target, CONSTITUTION)
    return target


def test_backup_restore_preserves_cited_answers(env, document, tmp_path):
    draft = import_doc(env, document)
    assert approve(env, draft).status_code == 200
    archive = snapshot(env, tmp_path)
    manifest, files = read_backup(archive)
    assert manifest["row_counts"]["sources"] == 1
    assert not any(".env" in name for name in files)
    engine = make_engine(f"sqlite+pysqlite:///{tmp_path / 'roundtrip_restore.sqlite'}")
    Base.metadata.create_all(engine)
    target = tmp_path / "vault_restore"
    try:
        assert restore_backup(engine, archive, target)["status"] == "restored"
        assert (target / "owner" / "note.md").read_bytes() == (env["root"] / "owner" / "note.md").read_bytes()
        with session_factory(engine)() as session:
            decision = respond(session, "owner", ChefRequest.model_validate(chef_body()))
        assert decision.citations[0].revision_id == draft["id"]
        assert decision.instruction == document["units"][0]["recommended_action"]
        with pytest.raises(ValueError, match="nonempty"):
            restore_backup(engine, archive, tmp_path / "second_restore")
    finally:
        engine.dispose()


def test_backup_checksum_and_path_guards(env, tmp_path):
    archive = snapshot(env, tmp_path)
    altered = tmp_path / "altered.zip"
    with ZipFile(archive) as original, ZipFile(altered, "w", ZIP_DEFLATED) as target:
        for info in original.infolist():
            target.writestr(info.filename, b"{}" if info.filename == "database.json" else original.read(info))
    with pytest.raises(ValueError, match="checksum"):
        read_backup(altered)
    unsafe = tmp_path / "unsafe.zip"
    with ZipFile(unsafe, "w") as target:
        target.writestr("../escape.md", "bad")
    with pytest.raises(ValueError, match="Unsafe"):
        read_backup(unsafe)


def test_backup_never_overwrites_or_includes_credentials(env, tmp_path):
    (env["root"] / ".env").write_text("PRIVATE_SECRET", encoding="utf-8")
    archive = snapshot(env, tmp_path)
    _, files = read_backup(archive)
    assert b"PRIVATE_SECRET" not in b"".join(files.values())
    with pytest.raises(FileExistsError):
        create_backup(env["engine"], env["root"], archive, CONSTITUTION)


def test_restore_refuses_ordinary_database_name(env, tmp_path):
    archive = snapshot(env, tmp_path)
    engine = make_engine(f"sqlite+pysqlite:///{tmp_path / 'ordinary.sqlite'}")
    try:
        with pytest.raises(ValueError, match="filename"):
            restore_backup(engine, archive, tmp_path / "vault_restore")
    finally:
        engine.dispose()


def test_backup_manifest_schema_rejected(env, tmp_path):
    archive = snapshot(env, tmp_path)
    changed = tmp_path / "future.zip"
    with ZipFile(archive) as original, ZipFile(changed, "w") as target:
        for info in original.infolist():
            data = original.read(info)
            if info.filename == "manifest.json":
                value = json.loads(data)
                value["schema_revision"] = "future"
                data = json.dumps(value).encode()
            target.writestr(info.filename, data)
    with pytest.raises(ValueError, match="schema"):
        read_backup(changed)
