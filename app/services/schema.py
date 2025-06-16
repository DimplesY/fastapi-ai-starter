from enum import Enum


class ServiceType(str, Enum):
    SETTINGS_SERVICE = "settings_service"
    DATABASE_SERVICE = "database_service"
