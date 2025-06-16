from __future__ import annotations

from app.services.factory import ServiceFactory
from app.services.database.service import DatabaseService
from app.services.settings.service import SettingsService


class DatabaseServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(DatabaseService)

    def create(self, settings_service: SettingsService):
        if not settings_service.settings.database_url:
            msg = "No database URL provided"
            raise ValueError(msg)
        return DatabaseService(settings_service)
