from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nickname: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    sessions: Mapped[list[AuthSession]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("length(nickname) BETWEEN 2 AND 20", name="ck_users_nickname_length"),
    )


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)

    user: Mapped[User] = relationship(back_populates="sessions")


class RecordMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class StudyRecord(RecordMixin, Base):
    __tablename__ = "study_records"

    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_studies_title_length"),
        CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_studies_content_length"),
        Index("ix_study_records_user_created", "user_id", "created_at"),
    )


class TodoRecord(RecordMixin, Base):
    __tablename__ = "todo_records"

    title: Mapped[str] = mapped_column(String(100))
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_todos_title_length"),
        CheckConstraint(
            "(is_completed = 0 AND completed_at IS NULL) OR "
            "(is_completed = 1 AND completed_at IS NOT NULL)",
            name="ck_todos_completed_time",
        ),
        Index("ix_todo_records_user_state_created", "user_id", "is_completed", "created_at"),
    )


class ErrorRecord(RecordMixin, Base):
    __tablename__ = "error_records"

    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    solution: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("length(title) BETWEEN 1 AND 100", name="ck_errors_title_length"),
        CheckConstraint("length(content) BETWEEN 1 AND 5000", name="ck_errors_content_length"),
        CheckConstraint(
            "solution IS NULL OR length(solution) BETWEEN 1 AND 5000",
            name="ck_errors_solution_length",
        ),
        CheckConstraint(
            "(is_resolved = 0 AND resolved_at IS NULL) OR "
            "(is_resolved = 1 AND solution IS NOT NULL AND resolved_at IS NOT NULL)",
            name="ck_errors_resolution",
        ),
        Index("ix_error_records_user_created", "user_id", "created_at"),
    )
