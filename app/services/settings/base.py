from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Annotated


class Settings(BaseSettings):
    environment: Annotated[str, Field(strict=True, alias="ENVIRONMENT")]
    database_url: Annotated[str, Field(strict=True, alias="DATABASE_URL")]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
