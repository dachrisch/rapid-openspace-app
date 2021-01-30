from datetime import timedelta, datetime
from typing import Union, Any

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import Provider

from rapidos.entity import Rapidos
from rapidos.service import RapidosService


class TestingRapidosCreationService(RapidosService):
    def __init__(self, id=1):
        super().__init__()
        self.id = id

    def create(self, name: str, duration: timedelta, sessions: int):
        self._instances[self.id] = Rapidos(name, datetime.now(), duration, sessions)
        return self.id


class OverridingContainer(DeclarativeContainer):
    creation_service = providers.Singleton(TestingRapidosCreationService)

    def __init__(self, **overriding_providers: Union[Provider, Any]):
        super().__init__(**overriding_providers)
        self.creation_service.create = lambda x: 1
