import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
NICKNAME_PATTERN = re.compile(r"^[가-힣A-Za-z0-9_]+$")


def normalize_email(value: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) > 320 or not EMAIL_PATTERN.fullmatch(normalized):
        raise ValueError("올바른 이메일 주소를 입력해 주세요.")
    return normalized


def normalize_nickname(value: str) -> str:
    normalized = value.strip()
    if not 2 <= len(normalized) <= 20:
        raise ValueError("닉네임은 2~20자로 입력해 주세요.")
    if not NICKNAME_PATTERN.fullmatch(normalized):
        raise ValueError("닉네임에는 한글, 영문, 숫자와 밑줄만 사용할 수 있습니다.")
    return normalized


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    nickname: str

    _email = field_validator("email")(normalize_email)
    _nickname = field_validator("nickname")(normalize_nickname)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=128)

    _email = field_validator("email")(normalize_email)


class NicknameUpdate(BaseModel):
    nickname: str

    _nickname = field_validator("nickname")(normalize_nickname)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nickname: str
    is_admin: bool
    created_at: datetime


class AuthResponse(BaseModel):
    token: str
    user: UserResponse
