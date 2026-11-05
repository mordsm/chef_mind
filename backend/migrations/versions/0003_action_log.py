"""Offline-capable, owner-scoped cooking action reports and retry receipts."""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"


def upgrade():
    op.create_table(
        "action_log_sessions",
        sa.Column("owner_id", sa.String(80), primary_key=True),
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("recipe_id", sa.String(80), nullable=False),
        sa.Column("linked_cooking_id", sa.String(80), nullable=False),
        sa.Column("revision", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "action_log_entries",
        sa.Column("owner_id", sa.String(80), primary_key=True),
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("cooking_id", sa.String(36), nullable=False),
        sa.Column("revision", sa.Integer, nullable=False),
        sa.Column("document", sa.JSON, nullable=False),
        sa.Column("deleted", sa.Integer, nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("alert_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_action_log_entries_cooking_id", "action_log_entries", ["cooking_id"])
    op.create_index("ix_action_log_entries_alert_at", "action_log_entries", ["alert_at"])
    op.create_table(
        "action_log_mutations",
        sa.Column("owner_id", sa.String(80), primary_key=True),
        sa.Column("request_id", sa.String(36), primary_key=True),
        sa.Column("body_hash", sa.String(64), nullable=False),
        sa.Column("result", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "web_push_subscriptions",
        sa.Column("owner_id", sa.String(80), primary_key=True),
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("document", sa.JSON, nullable=False),
        sa.Column("active", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "web_push_deliveries",
        sa.Column("owner_id", sa.String(80), primary_key=True),
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("report_id", sa.String(36), nullable=False),
        sa.Column("subscription_id", sa.String(64), nullable=False),
        sa.Column("target_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("lease_until", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("web_push_deliveries")
    op.drop_table("web_push_subscriptions")
    op.drop_table("action_log_mutations")
    op.drop_table("action_log_entries")
    op.drop_table("action_log_sessions")
