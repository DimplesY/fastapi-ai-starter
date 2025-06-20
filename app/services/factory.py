from __future__ import annotations

import importlib
import inspect
from typing import get_type_hints, TYPE_CHECKING

from app.services.schema import ServiceType

if TYPE_CHECKING:
    from app.services.base import Service


class ServiceFactory:
    def __init__(
        self,
        service_class,
    ) -> None:
        self.service_class = service_class
        self.dependencies = infer_service_types(self, import_all_services_into_a_dict())

    def create(self, *args, **kwargs) -> Service:
        raise self.service_class(*args, **kwargs)


def infer_service_types(factory: ServiceFactory, available_services=None) -> list[ServiceType]:
    create_method = factory.create
    type_hints = get_type_hints(create_method, globalns=available_services)
    service_types = []
    for param_name, param_type in type_hints.items():
        if param_name == "return":
            continue

        type_name = param_type.__name__.upper().replace("SERVICE", "_SERVICE")

        try:
            service_type = ServiceType[type_name]
            service_types.append(service_type)
        except KeyError as e:
            msg = f"No matching ServiceType for parameter type: {param_type.__name__}"
            raise ValueError(msg) from e
    return service_types


def import_all_services_into_a_dict():
    from app.services.base import Service

    services = {}
    for service_type in ServiceType:
        try:
            service_name = ServiceType(service_type).value.replace("_service", "")
            module_name = f"app.services.{service_name}.service"
            module = importlib.import_module(module_name)
            services.update(
                {
                    name: obj
                    for name, obj in inspect.getmembers(module, inspect.isclass)
                    if issubclass(obj, Service) and obj is not Service
                }
            )
        except Exception as exc:
            msg = "Could not initialize services. Please check your settings."
            raise RuntimeError(msg) from exc
    return services
