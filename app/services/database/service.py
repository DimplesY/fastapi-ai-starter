from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import sqlalchemy as sa
from alembic.config import Config
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from alembic import command
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
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=SQLModelAsyncSession,
            expire_on_commit=False,
        )

        self.project_dir = Path(__file__).parent.parent.parent.parent
        self.script_location = self.project_dir / "alembic"

    def _build_connection_kwargs(self):
        """Build connection kwargs by merging deprecated settings with db_connection_settings.

        Returns:
            dict: Connection kwargs with deprecated settings overriding db_connection_settings
        """
        settings = self.settings_service.settings
        connection_kwargs = settings.db_connection_settings.copy()

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
    async def with_session(self) -> AsyncGenerator[SQLModelAsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session

    @staticmethod
    def init_alembic(alembic_cfg) -> None:
        logger.info("Initializing alembic")
        command.ensure_version(alembic_cfg)
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic initialized")

    def _run_migrations(self) -> None:
        """Use Alembic to run migrations."""
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(self.script_location))
        alembic_cfg.set_main_option("sqlalchemy.url", self.database_url.replace("%", "%%"))
        try:
            self.init_alembic(alembic_cfg)
        except Exception as e:
            msg = "Error initializing alembic"
            logger.exception(msg)
            raise RuntimeError(msg) from e

    async def run_migrations(self) -> None:
        """Run database migrations."""
        await asyncio.to_thread(self._run_migrations)

    async def teardown(self) -> None:
        """Teardown the database engine."""
        await self.engine.dispose()
