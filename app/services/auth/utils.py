from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from asgiref.sync import sync_to_async
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.database.models.user import User
from app.services.database.models.user.crud import get_user_by_id
from app.services.deps import get_settings_service, injectable_session_scope

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_login = OAuth2PasswordBearer(tokenUrl="api/v1/login", auto_error=False)


@sync_to_async
def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


@sync_to_async
def password_verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    settings_service = get_settings_service()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings_service.settings.jwt_secret, algorithm=ALGORITHM)


@sync_to_async
def jwt_decode(token: str) -> Optional[int]:
    try:
        settings_service = get_settings_service()
        payload = jwt.decode(token, settings_service.settings.jwt_secret, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return int(user_id)
    except jwt.ExpiredSignatureError:
        return None


async def get_current_user(
    token: Annotated[str, Security(oauth2_login)],
    db: Annotated[AsyncSession, Depends(injectable_session_scope)],
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = await jwt_decode(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user
