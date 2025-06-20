from __future__ import annotations

from app.services.base import Service
from app.services.settings.service import SettingsService


class AuthService(Service):
    name = "auth_service"

    def __init__(self, settings_service: SettingsService):
        self.settings_service = settings_service
