from datetime import datetime, timedelta


class Rapidos(object):
    def __init__(self, name: str, start: datetime, duration: timedelta, sessions: int):
        self.sessions = sessions
        self.duration = duration
        self.start = start
        self.name = name

    def duration_formatted(self):
        return f'{self.duration.total_seconds() // 3600:.0f}h:{self.duration.total_seconds() / 60 % 60:.0f}m'
