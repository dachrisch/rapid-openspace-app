import uuid
from datetime import datetime, timedelta

from rapidos.entity import Rapidos, SessionLocation


class UUIDGenerator(object):
    def new_id(self) -> str:
        return str(uuid.uuid4())


class RapidosService(object):
    def __init__(self, id_generator: UUIDGenerator):
        self.id_generator = id_generator
        self._instances = {}

    def create(self, name: str, start: datetime, duration: timedelta, sessions: int):
        uuid_ = self.id_generator.new_id()
        rapidos = Rapidos(uuid_, name, start, duration, sessions)
        self._instances[uuid_] = rapidos
        return rapidos

    def get(self, uuid_: str) -> Rapidos:
        return self._instances[uuid_]

    def add_session_location(self, name):
        return SessionLocationBuilder(self, name)


class SessionLocationBuilder(object):
    def __init__(self, rapidos_service: RapidosService, name: str):
        self.rapidos_service = rapidos_service
        self.name = name

    def to(self, rapidos_id: str) -> SessionLocation:
        location = SessionLocation(self.rapidos_service.id_generator.new_id(), self.name)
        self.rapidos_service.get(rapidos_id).add_session_location(location)
        return location
