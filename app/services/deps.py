from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database.factory import DatabaseServiceFactory
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

    return get_service(ServiceType.SETTINGS_SERVICE, SettingsServiceFactory())


def get_db_service() -> DatabaseService:
    return get_service(ServiceType.DATABASE_SERVICE, DatabaseServiceFactory())


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_service().with_session() as session:
        yield session
