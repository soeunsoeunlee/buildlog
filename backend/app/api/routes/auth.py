from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import CurrentUser, Database
from app.core.security import create_session_token, hash_password, verify_password
from app.db.models import AuthSession, User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    NicknameUpdate,
    RegisterRequest,
    UserResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


def create_auth_response(db: Database, user: User) -> AuthResponse:
    token, token_hash, expires_at = create_session_token()
    db.add(AuthSession(token_hash=token_hash, user_id=user.id, expires_at=expires_at))
    db.commit()
    return AuthResponse(token=token, user=UserResponse.model_validate(user))


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Database) -> AuthResponse:
    existing = db.scalar(
        select(User).where(or_(User.email == payload.email, User.nickname == payload.nickname))
    )
    if existing is not None:
        if existing.email == payload.email:
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
        raise HTTPException(status_code=409, detail="이미 사용 중인 닉네임입니다.")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        nickname=payload.nickname,
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="이미 사용 중인 이메일 또는 닉네임입니다.") from exc
    return create_auth_response(db, user)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Database) -> AuthResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 맞지 않습니다.")
    return create_auth_response(db, user)


@router.get("/me", response_model=UserResponse)
def read_me(user: CurrentUser) -> User:
    return user


@router.patch("/me/nickname", response_model=UserResponse)
def update_nickname(payload: NicknameUpdate, user: CurrentUser, db: Database) -> User:
    existing = db.scalar(
        select(User).where(User.nickname == payload.nickname, User.id != user.id)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="이미 사용 중인 닉네임입니다.")
    user.nickname = payload.nickname
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="이미 사용 중인 닉네임입니다.") from exc
    db.refresh(user)
    return user
