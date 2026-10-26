from typing import Literal

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy import or_, select

from app.api.dependencies import CurrentUser, Database
from app.core.security import utc_now
from app.db.models import ErrorRecord, StudyRecord, TodoRecord
from app.schemas.records import (
    ErrorCreate,
    ErrorResponse,
    ErrorUpdate,
    StudyCreate,
    StudyResponse,
    StudyUpdate,
    TodoCreate,
    TodoResponse,
    TodoStatusUpdate,
    TodoUpdate,
)


study_router = APIRouter(prefix="/studies", tags=["studies"])
todo_router = APIRouter(prefix="/todos", tags=["todos"])
error_router = APIRouter(prefix="/errors", tags=["errors"])


def get_owned(db: Database, model, record_id: int, user_id: int):
    record = db.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    if record.user_id != user_id:
        raise HTTPException(status_code=403, detail="이 기록을 변경할 권한이 없습니다.")
    return record


def get_visible(db: Database, model, record_id: int, user_id: int):
    record = db.get(model, record_id)
    if record is None or (record.user_id != user_id and not record.is_public):
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    return record


@study_router.post("", response_model=StudyResponse, status_code=status.HTTP_201_CREATED)
def create_study(payload: StudyCreate, user: CurrentUser, db: Database) -> StudyRecord:
    record = StudyRecord(user_id=user.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@study_router.get("", response_model=list[StudyResponse])
def list_studies(
    user: CurrentUser,
    db: Database,
    q: str = Query(default="", max_length=100),
) -> list[StudyRecord]:
    query = select(StudyRecord).where(StudyRecord.user_id == user.id)
    term = q.strip()
    if term:
        pattern = f"%{term}%"
        query = query.where(
            or_(StudyRecord.title.ilike(pattern), StudyRecord.content.ilike(pattern))
        )
    return list(db.scalars(query.order_by(StudyRecord.created_at.desc(), StudyRecord.id.desc())))


@study_router.get("/{record_id}", response_model=StudyResponse)
def read_study(record_id: int, user: CurrentUser, db: Database) -> StudyRecord:
    return get_visible(db, StudyRecord, record_id, user.id)


@study_router.put("/{record_id}", response_model=StudyResponse)
def update_study(
    record_id: int, payload: StudyUpdate, user: CurrentUser, db: Database
) -> StudyRecord:
    record = get_owned(db, StudyRecord, record_id, user.id)
    for key, value in payload.model_dump().items():
        setattr(record, key, value)
    record.updated_at = utc_now()
    db.commit()
    db.refresh(record)
    return record


@study_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_study(record_id: int, user: CurrentUser, db: Database) -> Response:
    record = get_owned(db, StudyRecord, record_id, user.id)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@todo_router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, user: CurrentUser, db: Database) -> TodoRecord:
    record = TodoRecord(user_id=user.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@todo_router.get("", response_model=list[TodoResponse])
def list_todos(
    user: CurrentUser,
    db: Database,
    state: Literal["all", "pending", "completed"] = "all",
) -> list[TodoRecord]:
    query = select(TodoRecord).where(TodoRecord.user_id == user.id)
    if state == "pending":
        query = query.where(TodoRecord.is_completed.is_(False))
    elif state == "completed":
        query = query.where(TodoRecord.is_completed.is_(True))
    return list(
        db.scalars(
            query.order_by(
                TodoRecord.is_completed.asc(), TodoRecord.created_at.desc(), TodoRecord.id.desc()
            )
        )
    )


@todo_router.get("/{record_id}", response_model=TodoResponse)
def read_todo(record_id: int, user: CurrentUser, db: Database) -> TodoRecord:
    return get_visible(db, TodoRecord, record_id, user.id)


@todo_router.put("/{record_id}", response_model=TodoResponse)
def update_todo(
    record_id: int, payload: TodoUpdate, user: CurrentUser, db: Database
) -> TodoRecord:
    record = get_owned(db, TodoRecord, record_id, user.id)
    record.title = payload.title
    record.is_public = payload.is_public
    record.updated_at = utc_now()
    db.commit()
    db.refresh(record)
    return record


@todo_router.patch("/{record_id}/status", response_model=TodoResponse)
def update_todo_status(
    record_id: int, payload: TodoStatusUpdate, user: CurrentUser, db: Database
) -> TodoRecord:
    record = get_owned(db, TodoRecord, record_id, user.id)
    record.is_completed = payload.is_completed
    record.completed_at = utc_now() if payload.is_completed else None
    record.updated_at = utc_now()
    db.commit()
    db.refresh(record)
    return record


@todo_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(record_id: int, user: CurrentUser, db: Database) -> Response:
    record = get_owned(db, TodoRecord, record_id, user.id)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@error_router.post("", response_model=ErrorResponse, status_code=status.HTTP_201_CREATED)
def create_error(payload: ErrorCreate, user: CurrentUser, db: Database) -> ErrorRecord:
    record = ErrorRecord(user_id=user.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@error_router.get("", response_model=list[ErrorResponse])
def list_errors(
    user: CurrentUser,
    db: Database,
    state: Literal["all", "unresolved", "resolved"] = "all",
    q: str = Query(default="", max_length=100),
) -> list[ErrorRecord]:
    query = select(ErrorRecord).where(ErrorRecord.user_id == user.id)
    if state == "unresolved":
        query = query.where(ErrorRecord.is_resolved.is_(False))
    elif state == "resolved":
        query = query.where(ErrorRecord.is_resolved.is_(True))
    term = q.strip()
    if term:
        pattern = f"%{term}%"
        query = query.where(
            or_(ErrorRecord.title.ilike(pattern), ErrorRecord.content.ilike(pattern))
        )
    return list(db.scalars(query.order_by(ErrorRecord.created_at.desc(), ErrorRecord.id.desc())))


@error_router.get("/{record_id}", response_model=ErrorResponse)
def read_error(record_id: int, user: CurrentUser, db: Database) -> ErrorRecord:
    return get_visible(db, ErrorRecord, record_id, user.id)


@error_router.put("/{record_id}", response_model=ErrorResponse)
def update_error(
    record_id: int, payload: ErrorUpdate, user: CurrentUser, db: Database
) -> ErrorRecord:
    record = get_owned(db, ErrorRecord, record_id, user.id)
    was_resolved = record.is_resolved
    for key, value in payload.model_dump(exclude={"is_resolved"}).items():
        setattr(record, key, value)
    record.is_resolved = payload.is_resolved
    if payload.is_resolved and not was_resolved:
        record.resolved_at = utc_now()
    elif not payload.is_resolved:
        record.resolved_at = None
    record.updated_at = utc_now()
    db.commit()
    db.refresh(record)
    return record


@error_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_error(record_id: int, user: CurrentUser, db: Database) -> Response:
    record = get_owned(db, ErrorRecord, record_id, user.id)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
