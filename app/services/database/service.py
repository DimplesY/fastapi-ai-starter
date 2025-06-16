from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)

from app.services.base import Service
from app.services.settings.service import SettingsService


class DatabaseService(Service):
    name = "database_service"
    engine: AsyncEngine
    database_url: str

    def __init__(self, settings_service: SettingsService):
        self.settings_service = settings_service
        self.database_url: str = settings_service.settings.database_url
        self.engine = self.create_engine()

    def create_engine(self):
        return create_async_engine(self.database_url, echo=True)

    @asynccontextmanager
    async def with_session(self):
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            try:
                yield session
            except exc.SQLAlchemyError as db_exc:
                print(db_exc)
                await session.rollback()
                raise
