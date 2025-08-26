from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.database.models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    if isinstance(user_id, str):
        user_id = int(user_id)
    stmt = select(User).where(User.id == user_id)
    return (await db.execute(stmt)).scalar()
