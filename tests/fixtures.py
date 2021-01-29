from typing import Union, Any

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import Provider

from rapidos.service import RapidosCreationService


class TestingRapidosCreationService(RapidosCreationService):
    def __init__(self, id=1):
        self.id = id

    def create(self, name: str, count: int, length: int):
        return self.id


class OverridingContainer(DeclarativeContainer):
    creation_service = providers.Singleton(TestingRapidosCreationService)

    def __init__(self, **overriding_providers: Union[Provider, Any]):
        super().__init__(**overriding_providers)
        self.creation_service.create = lambda x: 1
