"""Private, immutable culinary source configuration revisions."""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"


def upgrade():
    op.create_table(
        "culinary_source_revisions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(80), nullable=False),
        sa.Column("source_key", sa.String(20), nullable=False),
        sa.Column("number", sa.Integer, nullable=False),
        sa.Column("yaml_text", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("owner_id", "source_key", "number"),
    )
    op.create_index("ix_culinary_source_revisions_owner_id", "culinary_source_revisions", ["owner_id"])


def downgrade():
    op.drop_table("culinary_source_revisions")
