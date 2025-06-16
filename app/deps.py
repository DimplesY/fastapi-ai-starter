from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.factory import DatabaseServiceFactory
from app.services.database.service import DatabaseService
from app.services.schema import ServiceType
from app.services.util import get_service


def get_db_service() -> DatabaseService:
    return get_service(ServiceType.DATABASE_SERVICE, DatabaseServiceFactory())


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_service().with_session() as session:
        yield session
