from datetime import datetime, timedelta
from typing import Dict


class SessionLocation(object):
    def __init__(self, _id: str, name: str):
        self.name = name
        self.id = _id


class Rapidos(object):
    def __init__(self, _id: str, name: str, start: datetime, duration: timedelta, sessions: int):
        self.id = _id
        self.sessions = sessions
        self._duration = duration
        self.start = start
        self.name = name
        self.locations :Dict[str, SessionLocation]= {}

    @property
    def duration(self) -> int:
        return int(self._duration.total_seconds() / 60)

    def add_session_location(self, session_location: SessionLocation):
        self.locations[session_location.id]=session_location

    def remove_session_location(self, location_id:str):
        self.locations.pop(location_id)
