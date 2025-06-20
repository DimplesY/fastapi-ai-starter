from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.services.database.models import User


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    if isinstance(user_id, str):
        user_id = int(user_id)
    stmt = select(User).where(User.id == user_id)
    return (await db.execute(stmt)).scalar()
