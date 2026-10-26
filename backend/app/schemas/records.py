from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def trimmed_required(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("공백이 아닌 내용을 입력해 주세요.")
    return normalized


def trimmed_optional(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


class StudyCreate(BaseModel):
    title: str = Field(max_length=100)
    content: str = Field(max_length=5000)
    is_public: bool = False

    _title = field_validator("title")(trimmed_required)
    _content = field_validator("content")(trimmed_required)


class StudyUpdate(StudyCreate):
    pass


class StudyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    is_public: bool
    created_at: datetime
    updated_at: datetime


class TodoCreate(BaseModel):
    title: str = Field(max_length=100)
    is_public: bool = False

    _title = field_validator("title")(trimmed_required)


class TodoUpdate(BaseModel):
    title: str = Field(max_length=100)
    is_public: bool

    _title = field_validator("title")(trimmed_required)


class TodoStatusUpdate(BaseModel):
    is_completed: bool


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_completed: bool
    is_public: bool
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ErrorCreate(BaseModel):
    title: str = Field(max_length=100)
    content: str = Field(max_length=5000)
    solution: str | None = Field(default=None, max_length=5000)
    is_public: bool = False

    _title = field_validator("title")(trimmed_required)
    _content = field_validator("content")(trimmed_required)
    _solution = field_validator("solution")(trimmed_optional)


class ErrorUpdate(ErrorCreate):
    is_resolved: bool

    @model_validator(mode="after")
    def solution_is_required_when_resolved(self) -> "ErrorUpdate":
        if self.is_resolved and self.solution is None:
            raise ValueError("해결 상태로 바꾸려면 해결 방법을 입력해 주세요.")
        return self


class ErrorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    solution: str | None
    is_resolved: bool
    is_public: bool
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime
