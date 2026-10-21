"""Read-only Vault reconciliation; imports are drafts, never activations or deletions."""

import hashlib
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db import Source
from app.knowledge import DomainError, audit, import_document, read_document
from app.schemas import ImportRequest


def reconcile(session, root: Path, owner: str):
    namespace = root / owner
    if not namespace.is_dir() or namespace.resolve().parent != root.resolve():
        raise DomainError("VAULT_UNAVAILABLE", "Owner Vault is unavailable", 503)
    files = sorted(namespace.rglob("*.md"))
    if len(files) > 1000:
        raise DomainError("VAULT_SCAN_LIMIT", "Split the Vault: maximum 1000 Markdown files per owner", 409)
    parsed, errors = [], []
    for path in files:
        relative = path.relative_to(namespace).as_posix()
        try:
            document, _, digest = read_document(root, owner, relative)
            parsed.append((relative, document.source_id, digest))
        except DomainError as exc:
            errors.append({"path": relative, "code": exc.code})
    counts = {}
    for _, source_id, _ in parsed:
        counts[source_id] = counts.get(source_id, 0) + 1
    imported, seen = [], set()
    for relative, source_id, digest in parsed:
        seen.add(source_id)
        if counts[source_id] != 1:
            errors.append({"path": relative, "code": "DUPLICATE_SOURCE_ID"})
            continue
        try:
            key = "sync-" + hashlib.sha256((relative + digest).encode()).hexdigest()
            revision = import_document(
                session, root, owner, ImportRequest(path=relative, idempotency_key=key)
            )
            # Re-read in import_document also prevents importing a stale file snapshot.
            imported.append({"path": relative, "revision_id": revision.id, "status": revision.status})
        except DomainError as exc:
            session.rollback()
            errors.append({"path": relative, "code": exc.code})
        except (SQLAlchemyError, OSError):
            session.rollback()
            errors.append({"path": relative, "code": "IMPORT_FAILED"})
    known = session.scalars(select(Source).where(Source.owner_id == owner)).all()
    missing = [source.source_id for source in known if source.source_id not in seen]
    report = {
        "items": imported,
        "errors": errors,
        "missing_sources": missing,
        "missing_action": "Kept active; human review required. No automatic deletion.",
    }
    audit(session, owner, "VAULT_RECONCILED", report=report)
    session.commit()
    return report
