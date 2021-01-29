import uuid


class RapidosCreationService(object):
    def create(self, name: str, count: int, length: int):
        return uuid.uuid4()
