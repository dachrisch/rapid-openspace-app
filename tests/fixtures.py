from rapidos import RapidosService, UUIDGenerator


class CreationServiceMock(RapidosService):
    def __init__(self, id_: str):
        super().__init__(MockIdGenerator(id_))


class MockIdGenerator(UUIDGenerator):

    def __init__(self, id_: str):
        self.id_ = id_

    def new_id(self) -> str:
        return self.id_