import uuid
from datetime import datetime, timedelta

from rapidos.entity import Rapidos


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

    def get(self, uuid_: str):
        return self._instances[uuid_]
