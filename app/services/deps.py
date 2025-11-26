from __future__ import annotations

from contextlib import asynccontextmanager, suppress
from typing import AsyncGenerator, cast

from sqlalchemy.exc import InvalidRequestError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.database.service import DatabaseService
from app.services.schema import ServiceType
from app.services.settings.service import SettingsService


def get_service(service_type: ServiceType, default=None):
    from app.services.manager import service_manager

    if not service_manager.factories:
        service_manager.register_factories()
    return service_manager.get(service_type, default)


def get_settings_service() -> SettingsService:
    from app.services.settings.factory import SettingsServiceFactory

    return cast(SettingsService, get_service(ServiceType.SETTINGS_SERVICE, SettingsServiceFactory()))


def get_db_service() -> DatabaseService:
    from app.services.database.factory import DatabaseServiceFactory

    return cast(DatabaseService, get_service(ServiceType.DATABASE_SERVICE, DatabaseServiceFactory()))


async def injectable_session_scope():
    async with session_scope() as session:
        yield session


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    session = get_db_service().session
    try:
        yield session
        await session.commit()
    except Exception:
        if session.is_active:
            with suppress(InvalidRequestError):
                await session.rollback()
        raise
