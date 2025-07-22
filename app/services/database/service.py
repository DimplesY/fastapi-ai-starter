from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sqlalchemy as sa
from loguru import logger
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
)

from app.services.base import Service
from app.services.settings.service import SettingsService


class DatabaseService(Service):
    name = "database_service"
    engine: AsyncEngine
    database_url: str

    def __init__(self, settings_service: SettingsService):
        self.settings_service = settings_service
        self.database_url: str = settings_service.settings.database_url
        self.engine = self._create_engine()

    def _build_connection_kwargs(self):
        """Build connection kwargs by merging deprecated settings with db_connection_settings.

        Returns:
            dict: Connection kwargs with deprecated settings overriding db_connection_settings
        """
        settings = self.settings_service.settings
        # Start with db_connection_settings as base
        connection_kwargs = settings.db_connection_settings.copy()

        # Override individual settings if explicitly set
        if "pool_size" in settings.model_fields_set:
            logger.warning("pool_size is deprecated. Use db_connection_settings['pool_size'] instead.")
            connection_kwargs["pool_size"] = settings.pool_size
        if "max_overflow" in settings.model_fields_set:
            logger.warning("max_overflow is deprecated. Use db_connection_settings['max_overflow'] instead.")
            connection_kwargs["max_overflow"] = settings.max_overflow

        return connection_kwargs

    def _create_engine(self) -> AsyncEngine:
        kwargs = self._build_connection_kwargs()

        poolclass_key = kwargs.get("poolclass")
        if poolclass_key is not None:
            pool_class = getattr(sa, poolclass_key, None)
            if pool_class and isinstance(pool_class(), sa.pool.Pool):
                logger.debug(f"Using poolclass: {poolclass_key}.")
                kwargs["poolclass"] = pool_class
            else:
                logger.error(f"Invalid poolclass '{poolclass_key}' specified. Using default pool class.")

        return create_async_engine(self.database_url, **kwargs)

    @asynccontextmanager
    async def with_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            try:
                yield session
            except exc.SQLAlchemyError as db_exc:
                print(db_exc)
                await session.rollback()
                raise
