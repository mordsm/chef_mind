"""Initial reviewed knowledge and isolated cooking state."""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None


def upgrade():
    postgres = op.get_bind().dialect.name == "postgresql"
    if postgres:
        op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "sources",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(80), nullable=False),
        sa.Column("source_id", sa.String(80), nullable=False),
        sa.Column("path", sa.Text, nullable=False),
        sa.Column("active_revision_id", sa.String(36)),
        sa.UniqueConstraint("owner_id", "source_id"),
    )
    op.create_table(
        "revisions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_pk", sa.String(36), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("document", sa.JSON, nullable=False),
        sa.Column("markdown", sa.Text, nullable=False),
        sa.Column("gate_result", sa.JSON),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_pk", "number"),
        sa.UniqueConstraint("source_pk", "content_hash"),
    )
    op.create_table(
        "indexed_units",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("revision_id", sa.String(36), sa.ForeignKey("revisions.id"), nullable=False),
        sa.Column("knowledge_id", sa.String(80), nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("embedding", Vector(384) if postgres else sa.JSON, nullable=False),
        sa.UniqueConstraint("revision_id", "knowledge_id"),
    )
    op.create_table(
        "import_keys",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(80), nullable=False),
        sa.Column("key", sa.String(100), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("revision_id", sa.String(36), sa.ForeignKey("revisions.id"), nullable=False),
        sa.UniqueConstraint("owner_id", "key"),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(80), nullable=False),
        sa.Column("action", sa.String(80), nullable=False),
        sa.Column("details", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "cooking_records",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(80), nullable=False),
        sa.Column("cooking_id", sa.String(80), nullable=False),
        sa.Column("revision", sa.Integer, nullable=False),
        sa.Column("state", sa.JSON, nullable=False),
        sa.Column("decision", sa.JSON, nullable=False),
        sa.UniqueConstraint("owner_id", "cooking_id"),
    )
    for table, column in [
        ("sources", "owner_id"),
        ("revisions", "source_pk"),
        ("revisions", "status"),
        ("indexed_units", "revision_id"),
        ("audit_events", "owner_id"),
        ("cooking_records", "owner_id"),
    ]:
        op.create_index(f"ix_{table}_{column}", table, [column])
    if postgres:
        op.execute(
            "CREATE INDEX ix_units_text_search ON indexed_units USING gin(to_tsvector('simple', text))"
        )


def downgrade():
    for table in ("cooking_records", "audit_events", "import_keys", "indexed_units", "revisions", "sources"):
        op.drop_table(table)
