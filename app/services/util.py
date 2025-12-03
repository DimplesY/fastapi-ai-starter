from __future__ import annotations

from app.services.database.utils import initialize_database
from app.services.deps import get_service
from app.services.manager import service_manager
from app.services.schema import ServiceType


def initialize_settings_service() -> None:
    from app.services.settings import factory as settings_factory

    get_service(ServiceType.SETTINGS_SERVICE, settings_factory.SettingsServiceFactory())


async def initialize_services() -> None:
    await initialize_database()


async def teardown_services() -> None:
    """Teardown all the services."""
    await service_manager.teardown()
