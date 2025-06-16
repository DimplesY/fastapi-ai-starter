import importlib
import inspect
from app.services.base import Service
from app.services.factory import ServiceFactory
from app.services.schema import ServiceType


class ServiceManager:
    def __init__(self) -> None:
        self.services: dict[str, Service] = {}
        self.factories: dict[str, ServiceFactory] = {}
        self.register_factories()

    def register_factories(self) -> None:
        for factory in self.get_factories():
            try:
                self.register_factory(factory)
            except Exception:
                print(f"Failed to register factory: {factory}")

    def register_factory(
        self,
        service_factory: ServiceFactory,
    ) -> None:
        service_name = service_factory.service_class.name
        self.factories[service_name] = service_factory

    def get(self, service_name: ServiceType, default: ServiceFactory | None = None) -> Service:
        if service_name not in self.services:
            self._create_service(service_name, default)
        return self.services[service_name]

    def _create_service(self, service_name: ServiceType, default: ServiceFactory | None = None) -> None:
        self._validate_service_creation(service_name, default)

        factory = self.factories.get(service_name)
        if factory is None and default is not None:
            self.register_factory(default)
            factory = default
        if factory is None:
            msg = f"No factory registered for {service_name}"
            raise RuntimeError(msg)
        for dependency in factory.dependencies:
            if dependency not in self.services:
                self._create_service(dependency)

        dependent_services = {dep.value: self.services[dep] for dep in factory.dependencies}

        self.services[service_name] = self.factories[service_name].create(**dependent_services)
        self.services[service_name].set_ready()

    def _validate_service_creation(self, service_name: ServiceType, default: ServiceFactory | None = None) -> None:
        if service_name not in self.factories and default is None:
            msg = f"No factory registered for the service class '{service_name.name}'"
            raise RuntimeError(msg)

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
                        factories.append(obj())
                        break

            except Exception as exc:
                msg = f"Could not initialize services. Please check your settings. Error in {name}."
                raise RuntimeError(msg) from exc

        return factories


service_manager = ServiceManager()
