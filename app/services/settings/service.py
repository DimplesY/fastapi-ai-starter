from __future__ import annotations

from app.services.base import Service
from app.services.settings.base import Settings


class SettingsService(Service):
    name = "settings_service"

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings: Settings = settings

    @classmethod
    def initialize(cls) -> SettingsService:
        settings = Settings()  # type: ignore
        return cls(settings)

    def set(self, key, value):
        setattr(self.settings, key, value)
        return self.settings
