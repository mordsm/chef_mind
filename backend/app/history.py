"""Owner-scoped immutable source history and reversible index lifecycle."""

import difflib

from sqlalchemy import select

from app.db import IndexedUnit, Revision
from app.knowledge import DomainError, audit, owned_revision, revision_payload, unit_text
from app.schemas import KnowledgeDocument


def source_history(session, owner, revision_id):
    _, source = owned_revision(session, owner, revision_id)
    revisions = session.scalars(
        select(Revision).where(Revision.source_pk == source.id).order_by(Revision.number.desc())
    ).all()
    return {
        "source_id": source.source_id,
        "active_revision_id": source.active_revision_id,
        "items": [revision_payload(row) for row in revisions],
    }


def revision_diff(session, owner, revision_id, other_id):
    revision, source = owned_revision(session, owner, revision_id)
    other, other_source = owned_revision(session, owner, other_id)
    if source.id != other_source.id:
        raise DomainError("SOURCE_MISMATCH", "Compare revisions of the same source", 409)
    # Markdown is already capped at 256 KiB by import. Return text, never HTML.
    diff = "\n".join(
        difflib.unified_diff(
            other.markdown.splitlines(),
            revision.markdown.splitlines(),
            fromfile=f"revision-{other.number}",
            tofile=f"revision-{revision.number}",
            lineterm="",
        )
    )
    return {
        "source_id": source.source_id,
        "from_revision_id": other.id,
        "to_revision_id": revision.id,
        "diff": diff,
    }


def lifecycle(session, owner, revision_id, request, operation, embed, gate):
    # All lifecycle/approval operations serialize on this same source row.
    revision, source = owned_revision(session, owner, revision_id, lock=True)
    if source.active_revision_id != request.expected_active_revision_id:
        raise DomainError("ACTIVE_REVISION_CONFLICT", "Active knowledge changed; reload source history", 409)
    previous_id = source.active_revision_id
    if operation == "retire":
        if previous_id != revision.id or revision.status != "active":
            raise DomainError("NOT_ACTIVE", "Only the current active revision can be retired", 409)
        revision.status = "retired"
        source.active_revision_id = None
        # Historical index rows and cooking citations are deliberately retained.
    else:
        if revision.status not in {"superseded", "retired"} or not revision.gate_result:
            raise DomainError(
                "ROLLBACK_NOT_APPROVED", "Rollback requires a previously approved revision", 409
            )
        document = KnowledgeDocument.model_validate(revision.document)
        if document.license_status == "unknown" or any(unit.conflicts_with for unit in document.units):
            raise DomainError("ROLLBACK_SOURCE_UNSAFE", "Resolve license or declared conflicts first", 409)
        result = gate(document)
        if not result["passed"]:
            audit(session, owner, "ROLLBACK_GATE_FAILED", revision_id=revision.id, result=result)
            session.commit()
            raise DomainError("REGRESSION_GATE_FAILED", "Rollback failed current activation checks", 409)
        indexed = session.scalars(select(IndexedUnit).where(IndexedUnit.revision_id == revision.id)).all()
        # Rebuild vectors locally before changing the pointer; failures roll back the transaction.
        by_id = {item.knowledge_id: item for item in indexed}
        for unit in document.units:
            vector = embed(unit_text(unit))
            row = by_id.get(unit.knowledge_id)
            if row is None:
                row = IndexedUnit(revision_id=revision.id, knowledge_id=unit.knowledge_id)
                session.add(row)
            row.text, row.embedding = unit_text(unit), vector
        if previous_id:
            session.get(Revision, previous_id).status = "superseded"
        revision.status, revision.gate_result = "active", result
        source.active_revision_id = revision.id
    audit(
        session,
        owner,
        "KNOWLEDGE_RETIRED" if operation == "retire" else "KNOWLEDGE_ROLLED_BACK",
        revision_id=revision.id,
        previous_active_revision_id=previous_id,
        reason=request.reason,
    )
    session.commit()
    return revision_payload(revision)
