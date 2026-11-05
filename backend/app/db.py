from datetime import UTC, datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool


def uid():
    return str(uuid4())


def now():
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class CulinarySourceRevision(Base):
    __tablename__ = "culinary_source_revisions"
    __table_args__ = (UniqueConstraint("owner_id", "source_key", "number"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(String(80), index=True)
    source_key: Mapped[str] = mapped_column(String(20))
    number: Mapped[int] = mapped_column(Integer)
    yaml_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Source(Base):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("owner_id", "source_id"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(String(80), index=True)
    source_id: Mapped[str] = mapped_column(String(80))
    path: Mapped[str] = mapped_column(Text)
    active_revision_id: Mapped[str | None] = mapped_column(String(36), nullable=True)


class Revision(Base):
    __tablename__ = "revisions"
    __table_args__ = (UniqueConstraint("source_pk", "number"), UniqueConstraint("source_pk", "content_hash"))
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    source_pk: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    number: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(30), default="pending_review", index=True)
    document: Mapped[dict] = mapped_column(JSON)
    markdown: Mapped[str] = mapped_column(Text)
    gate_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class IndexedUnit(Base):
    __tablename__ = "indexed_units"
    __table_args__ = (UniqueConstraint("revision_id", "knowledge_id"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    revision_id: Mapped[str] = mapped_column(ForeignKey("revisions.id"), index=True)
    knowledge_id: Mapped[str] = mapped_column(String(80))
    text: Mapped[str] = mapped_column(Text)
    # SQLite is a clearly separated portable test adapter, not a pgvector substitute claim.
    embedding: Mapped[list] = mapped_column(Vector(384).with_variant(JSON(), "sqlite"))


class ImportKey(Base):
    __tablename__ = "import_keys"
    __table_args__ = (UniqueConstraint("owner_id", "key"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(String(80))
    key: Mapped[str] = mapped_column(String(100))
    content_hash: Mapped[str] = mapped_column(String(64))
    revision_id: Mapped[str] = mapped_column(ForeignKey("revisions.id"))


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(String(80), index=True)
    action: Mapped[str] = mapped_column(String(80))
    details: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class CookingRecord(Base):
    __tablename__ = "cooking_records"
    __table_args__ = (UniqueConstraint("owner_id", "cooking_id"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(String(80), index=True)
    cooking_id: Mapped[str] = mapped_column(String(80))
    revision: Mapped[int] = mapped_column(Integer, default=0)
    state: Mapped[dict] = mapped_column(JSON)
    decision: Mapped[dict] = mapped_column(JSON)


class ActionLogSession(Base):
    __tablename__ = "action_log_sessions"
    owner_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    recipe_id: Mapped[str] = mapped_column(String(80), default="")
    linked_cooking_id: Mapped[str] = mapped_column(String(80), default="")
    revision: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ActionLogEntry(Base):
    __tablename__ = "action_log_entries"
    owner_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    cooking_id: Mapped[str] = mapped_column(String(36), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    document: Mapped[dict] = mapped_column(JSON)
    deleted: Mapped[int] = mapped_column(Integer, default=0)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    alert_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class ActionLogMutation(Base):
    __tablename__ = "action_log_mutations"
    owner_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    body_hash: Mapped[str] = mapped_column(String(64))
    result: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class WebPushSubscription(Base):
    __tablename__ = "web_push_subscriptions"
    owner_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document: Mapped[dict] = mapped_column(JSON)
    active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class WebPushDelivery(Base):
    __tablename__ = "web_push_deliveries"
    owner_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    report_id: Mapped[str] = mapped_column(String(36))
    subscription_id: Mapped[str] = mapped_column(String(64))
    target_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    next_attempt_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    lease_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


def make_engine(url):
    options = {}
    if url.startswith("postgresql"):
        options["connect_args"] = {"connect_timeout": 5}
    if url.startswith("sqlite"):
        options["connect_args"] = {"check_same_thread": False}
        if ":memory:" in url:
            options["poolclass"] = StaticPool
    return create_engine(url, pool_pre_ping=True, **options)


def session_factory(engine):
    return sessionmaker(engine, expire_on_commit=False)
