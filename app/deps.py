from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import db


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.with_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_session)]
