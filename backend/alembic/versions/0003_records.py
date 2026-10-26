"""Add study, todo and error records.

Revision ID: 0003_records
Revises: 0002_users_and_sessions
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0003_records"
down_revision: str | None = "0002_users_and_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def common_columns() -> list[sa.Column]:
    return [
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_public", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "study_records",
        *common_columns(),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_studies_content_length"),
        sa.CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_studies_title_length"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_study_records_user_created", "study_records", ["user_id", "created_at"])
    op.create_index(op.f("ix_study_records_created_at"), "study_records", ["created_at"])
    op.create_index(op.f("ix_study_records_user_id"), "study_records", ["user_id"])

    op.create_table(
        "todo_records",
        *common_columns(),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("is_completed", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_todos_title_length"),
        sa.CheckConstraint(
            "(is_completed = 0 AND completed_at IS NULL) OR "
            "(is_completed = 1 AND completed_at IS NOT NULL)",
            name="ck_todos_completed_time",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todo_records_user_state_created", "todo_records", ["user_id", "is_completed", "created_at"])
    op.create_index(op.f("ix_todo_records_created_at"), "todo_records", ["created_at"])
    op.create_index(op.f("ix_todo_records_user_id"), "todo_records", ["user_id"])

    op.create_table(
        "error_records",
        *common_columns(),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("solution", sa.Text(), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), server_default="0", nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_errors_title_length"),
        sa.CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_errors_content_length"),
        sa.CheckConstraint("solution IS NULL OR length(solution) BETWEEN 1 AND 5000", name="ck_errors_solution_length"),
        sa.CheckConstraint(
            "(is_resolved = 0 AND resolved_at IS NULL) OR "
            "(is_resolved = 1 AND solution IS NOT NULL AND resolved_at IS NOT NULL)",
            name="ck_errors_resolution",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_error_records_user_created", "error_records", ["user_id", "created_at"])
    op.create_index(op.f("ix_error_records_created_at"), "error_records", ["created_at"])
    op.create_index(op.f("ix_error_records_user_id"), "error_records", ["user_id"])


def downgrade() -> None:
    op.drop_table("error_records")
    op.drop_table("todo_records")
    op.drop_table("study_records")
