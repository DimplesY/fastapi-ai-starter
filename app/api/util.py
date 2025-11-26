from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.auth.utils import get_current_user
from app.services.database.models.user import User
from app.services.deps import injectable_session_scope

DbSession = Annotated[AsyncSession, Depends(injectable_session_scope)]
CurrentUser = Annotated[User, Depends(get_current_user)]
