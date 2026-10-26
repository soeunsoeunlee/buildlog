from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_token, utc_now
from app.db.models import AuthSession, User
from app.db.session import get_db


bearer_scheme = HTTPBearer(auto_error=False)
Database = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: Database,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    auth_session = db.scalar(
        select(AuthSession).where(AuthSession.token_hash == hash_token(credentials.credentials))
    )
    if auth_session is None or auth_session.expires_at <= utc_now():
        raise HTTPException(status_code=401, detail="로그인이 만료되었습니다. 다시 로그인해 주세요.")

    user = db.get(User, auth_session.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="사용자 정보를 찾을 수 없습니다.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
