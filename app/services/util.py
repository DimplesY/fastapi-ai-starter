from __future__ import annotations

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


def initialize_settings_service() -> None:
    from app.services.settings import factory as settings_factory

    get_service(ServiceType.SETTINGS_SERVICE, settings_factory.SettingsServiceFactory())


async def initialize_services() -> None:
    initialize_settings_service()
