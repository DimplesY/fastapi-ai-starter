from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Annotated


class Settings(BaseSettings):
    environment: Annotated[str, Field(strict=True, alias="ENVIRONMENT")]
    database_url: Annotated[str, Field(strict=True, alias="DATABASE_URL")]
    jwt_secret: Annotated[str, Field(strict=True, alias="JWT_SECRET")]
    db_connection_settings: dict | None = {
        "pool_size": 20,  # Match the pool_size above
        "max_overflow": 30,  # Match the max_overflow above
        "pool_timeout": 30,  # Seconds to wait for a connection from pool
        "pool_pre_ping": True,  # Check connection validity before using
        "pool_recycle": 1800,  # Recycle connections after 30 minutes
        "echo": False,  # Set to True for debugging only
    }
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
