"""Immutable source revisions. Only explicit review can activate indexed knowledge."""

import hashlib
from pathlib import Path

import yaml
from sqlalchemy import delete, func, select

from app.db import AuditEvent, ImportKey, IndexedUnit, Revision, Source
from app.schemas import KnowledgeDocument


class DomainError(Exception):
    def __init__(self, code, message, status=400):
        self.code, self.message, self.status = code, message, status


def audit(session, owner, action, **details):
    event = AuditEvent(owner_id=owner, action=action, details=details)
    session.add(event)
    return event


def read_document(root: Path, owner: str, relative: str):
    if ":" in relative or Path(relative).is_absolute():
        raise DomainError("INVALID_PATH", "Use a relative Markdown path inside your vault")
    allowed = (root / owner).resolve()
    if allowed.parent != root.resolve() or allowed.name != owner:
        raise DomainError("INVALID_PATH", "User vault root must not redirect to another namespace")
    path = (allowed / relative).resolve()
    if not path.is_relative_to(allowed) or path.suffix.lower() != ".md":
        raise DomainError("INVALID_PATH", "Use a Markdown file inside your own vault")
    try:
        with path.open("rb") as stream:
            raw = stream.read(262_145)
    except OSError as exc:
        raise DomainError("SOURCE_UNAVAILABLE", "Markdown source is not available", 404) from exc
    if len(raw) > 262_144:
        raise DomainError("SOURCE_TOO_LARGE", "Markdown files are limited to 256 KiB")
    try:
        markdown = raw.decode("utf-8-sig")
        if not markdown.startswith("---\n") and not markdown.startswith("---\r\n"):
            raise ValueError("Missing frontmatter")
        parts = markdown.split("---", 2)
        if len(parts) != 3:
            raise ValueError("Missing frontmatter terminator")
        document = KnowledgeDocument.model_validate(yaml.safe_load(parts[1]))
    except (UnicodeError, ValueError, yaml.YAMLError, RecursionError) as exc:
        raise DomainError(
            "INVALID_DOCUMENT", "Invalid UTF-8 Markdown/frontmatter or knowledge fields"
        ) from exc
    return document, markdown, hashlib.sha256(raw).hexdigest()


def revision_payload(revision):
    return {
        "id": revision.id,
        "revision": revision.number,
        "status": revision.status,
        "document": revision.document,
        "content_hash": revision.content_hash,
        "gate_result": revision.gate_result,
    }


def import_document(session, root, owner, request):
    document, markdown, digest = read_document(root, owner, request.path)
    previous_key = session.scalar(
        select(ImportKey).where(ImportKey.owner_id == owner, ImportKey.key == request.idempotency_key)
    )
    if previous_key:
        if previous_key.content_hash != digest:
            raise DomainError("IDEMPOTENCY_CONFLICT", "This key was already used for different content", 409)
        return session.get(Revision, previous_key.revision_id)
    source = session.scalar(
        select(Source)
        .where(Source.owner_id == owner, Source.source_id == document.source_id)
        .with_for_update()
    )
    if source is None:
        source = Source(owner_id=owner, source_id=document.source_id, path=request.path)
        session.add(source)
        session.flush()
    revision = session.scalar(
        select(Revision).where(Revision.source_pk == source.id, Revision.content_hash == digest)
    )
    if revision is None:
        number = (
            session.scalar(select(func.max(Revision.number)).where(Revision.source_pk == source.id)) or 0
        ) + 1
        revision = Revision(
            source_pk=source.id,
            number=number,
            content_hash=digest,
            document=document.model_dump(),
            markdown=markdown,
        )
        session.add(revision)
        session.flush()
        audit(session, owner, "SOURCE_IMPORTED", revision_id=revision.id, source_id=document.source_id)
    source.path = request.path
    session.add(
        ImportKey(owner_id=owner, key=request.idempotency_key, content_hash=digest, revision_id=revision.id)
    )
    session.commit()
    return revision


def owned_revision(session, owner, revision_id, lock=False):
    query = (
        select(Revision, Source)
        .join(Source, Source.id == Revision.source_pk)
        .where(Source.owner_id == owner, Revision.id == revision_id)
    )
    if lock:
        query = query.with_for_update()
    result = session.execute(query).first()
    if result is None:
        raise DomainError("NOT_FOUND", "Knowledge revision was not found", 404)
    return result


def review_revision(session, owner, revision_id, request, approve, embed, gate):
    revision, source = owned_revision(session, owner, revision_id, lock=True)
    latest = session.scalar(select(func.max(Revision.number)).where(Revision.source_pk == source.id))
    if revision.number != request.expected_revision or revision.number != latest:
        raise DomainError(
            "REVISION_CONFLICT", "Review the latest source revision before changing its status", 409
        )
    if revision.status != "pending_review":
        raise DomainError("ALREADY_REVIEWED", "This revision already has a review decision", 409)
    if not approve:
        revision.status = "rejected"
        audit(session, owner, "KNOWLEDGE_REJECTED", revision_id=revision.id, reason=request.reason)
        session.commit()
        return revision
    document = KnowledgeDocument.model_validate(revision.document)
    if document.license_status == "unknown":
        raise DomainError(
            "LICENSE_UNVERIFIED", "License authorization must be reviewed before activation", 409
        )
    if any(unit.conflicts_with for unit in document.units):
        raise DomainError("UNRESOLVED_CONFLICT", "Resolve declared source contradictions in a new draft", 409)
    # This baseline embedding is local and bounded. No network call occurs under the lock.
    candidate = [(unit, embed(unit_text(unit))) for unit in document.units]
    gate_result = gate(document)
    if not gate_result["passed"]:
        audit(session, owner, "ACTIVATION_GATE_FAILED", revision_id=revision.id, result=gate_result)
        session.commit()
        raise DomainError(
            "REGRESSION_GATE_FAILED", "Candidate failed activation checks; existing index remains active", 409
        )
    session.execute(delete(IndexedUnit).where(IndexedUnit.revision_id == revision.id))
    for unit, vector in candidate:
        session.add(
            IndexedUnit(
                revision_id=revision.id,
                knowledge_id=unit.knowledge_id,
                text=unit_text(unit),
                embedding=vector,
            )
        )
    if source.active_revision_id:
        previous = session.get(Revision, source.active_revision_id)
        previous.status = "superseded"
    revision.status = "active"
    revision.gate_result = gate_result
    source.active_revision_id = revision.id
    audit(
        session,
        owner,
        "KNOWLEDGE_APPROVED_ACTIVATED",
        revision_id=revision.id,
        reason=request.reason,
        gate=gate_result,
    )
    session.commit()
    return revision


def unit_text(unit):
    return " ".join(
        [
            unit.title,
            unit.principle,
            *unit.tags,
            *unit.conditions,
            unit.recommended_action,
            *unit.observations,
        ]
    )


def active_rows(session, owner):
    return (
        select(IndexedUnit, Revision, Source)
        .join(Revision, Revision.id == IndexedUnit.revision_id)
        .join(Source, Source.id == Revision.source_pk)
        .where(
            Source.owner_id == owner, Source.active_revision_id == Revision.id, Revision.status == "active"
        )
    )
