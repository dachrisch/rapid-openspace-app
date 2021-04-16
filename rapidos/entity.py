from datetime import datetime, timedelta


class Rapidos(object):
    def __init__(self, _id: str, name: str, start: datetime, duration: timedelta, sessions: int):
        self.id = _id
        self.sessions = sessions
        self._duration = duration
        self.start = start
        self.name = name

    @property
    def duration(self) -> int:
        return int(self._duration.total_seconds() / 60)


class Room(object):
    def __init__(self, name: str):
        self.name = name
