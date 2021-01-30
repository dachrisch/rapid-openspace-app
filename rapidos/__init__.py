from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from rapidos.service import RapidosService


class Container(DeclarativeContainer):
    creation_service = providers.Singleton(RapidosService)
