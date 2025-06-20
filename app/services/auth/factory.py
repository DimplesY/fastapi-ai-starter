from __future__ import annotations

from app.services.auth.service import AuthService
from app.services.factory import ServiceFactory
from app.services.settings.service import SettingsService


class AuthServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(AuthService)

    def create(self, settings_service: SettingsService):
        return AuthService(settings_service)
