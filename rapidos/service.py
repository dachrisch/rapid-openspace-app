import uuid
from datetime import datetime, timedelta

from rapidos.entity import Rapidos


class RapidosService(object):
    def __init__(self):
        self._instances = {}

    def create(self, name: str, start: datetime, duration: timedelta, sessions: int):
        uuid_ = uuid.uuid4()
        self._instances[uuid_] = Rapidos(name, start, duration, sessions)
        return uuid_

    def get(self, uuid_: str):
        return self._instances[uuid.UUID(uuid_)]
