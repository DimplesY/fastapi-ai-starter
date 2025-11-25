from __future__ import annotations

import asyncio
import importlib
import inspect
from typing import TYPE_CHECKING

from app.logging import logger
from app.util.concurrency import KeyedMemoryLockManager

if TYPE_CHECKING:
    from app.services.base import Service
    from app.services.factory import ServiceFactory
    from app.services.schema import ServiceType


class NoFactoryRegisteredError(Exception):
    pass


class ServiceManager:
    def __init__(self) -> None:
        self.services: dict[str, Service] = {}
        self.factories: dict[str, ServiceFactory] = {}
        self.register_factories()
        self.keyed_lock = KeyedMemoryLockManager()

    def register_factories(self) -> None:
        for factory in self.get_factories():
            try:
                self.register_factory(factory)
            except Exception:  # noqa: BLE001
                logger.exception(f"Error initializing {factory}")

    def register_factory(
        self,
        service_factory: ServiceFactory,
    ) -> None:
        service_name = service_factory.service_class.name
        self.factories[service_name] = service_factory

    def get(self, service_name: ServiceType, default: ServiceFactory | None = None) -> Service:
        with self.keyed_lock.lock(service_name):
            if service_name not in self.services:
                self._create_service(service_name, default)
        return self.services[service_name]

    def _create_service(self, service_name: ServiceType, default: ServiceFactory | None = None) -> None:
        logger.debug(f"Create service {service_name}")
        self._validate_service_creation(service_name, default)

        factory = self.factories.get(service_name)
        if factory is None and default is not None:
            self.register_factory(default)
            factory = default
        if factory is None:
            msg = f"No factory registered for {service_name}"
            raise NoFactoryRegisteredError(msg)
        for dependency in factory.dependencies:
            if dependency not in self.services:
                self._create_service(dependency)

        dependent_services = {dep.value: self.services[dep] for dep in factory.dependencies}

        self.services[service_name] = self.factories[service_name].create(**dependent_services)
        self.services[service_name].set_ready()

    def _validate_service_creation(self, service_name: ServiceType, default: ServiceFactory | None = None) -> None:
        if service_name not in self.factories and default is None:
            msg = f"No factory registered for the service class '{service_name.name}'"
            raise NoFactoryRegisteredError(msg)

    async def teardown(self) -> None:
        """Teardown all the services."""
        for service in list(self.services.values()):
            if service is None:
                continue
            logger.debug(f"Teardown service {service.name}")
            try:
                teardown_result = service.teardown()
                if asyncio.iscoroutine(teardown_result):
                    await teardown_result
            except Exception as exc:  # noqa: BLE001
                logger.debug(f"Error in teardown of {service.name}", exc_info=exc)
        self.services = {}
        self.factories = {}

    @staticmethod
    def get_factories():
        from app.services.factory import ServiceFactory
        from app.services.schema import ServiceType

        service_names = [ServiceType(service_type).value.replace("_service", "") for service_type in ServiceType]
        base_module = "app.services"
        factories = []

        for name in service_names:
            try:
                module_name = f"{base_module}.{name}.factory"
                module = importlib.import_module(module_name)

                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, ServiceFactory) and obj is not ServiceFactory:
                        factories.append(obj())  # type: ignore
                        break

            except Exception as exc:
                logger.exception(exc)
                msg = f"Could not initialize services. Please check your settings. Error in {name}."
                raise RuntimeError(msg) from exc

        return factories


service_manager = ServiceManager()
