import uuid
from datetime import datetime, timedelta

from rapidos.entity import Rapidos, Room


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

    def add_room(self, name):
        return RoomBuilder(self, name)


class RoomBuilder(object):
    def __init__(self, rapidos_service: RapidosService, name):
        self.rapidos_service = rapidos_service
        self.name = name

    def to(self, rapidos_id: str) -> Room:
        room = Room(self.rapidos_service.id_generator.new_id(), self.name)
        self.rapidos_service.get(rapidos_id).add_room(room)
        return room
