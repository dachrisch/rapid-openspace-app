import uuid
from datetime import datetime, timedelta
from unittest import TestCase

import pytest as pytest

from rapidos import RapidosService
from rapidos.service import UUIDGenerator
from rapidos.web import create_app


class MockIdGenerator(UUIDGenerator):

    def __init__(self, id_: str):
        self.id_ = id_

    def new_id(self) -> str:
        return self.id_


class CreationServiceMock(RapidosService):
    def __init__(self, id_: str):
        super().__init__(MockIdGenerator(id_))


class TestRapidosApi(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # XXX: workaround, cause API lazy init is not working correctly
        # when app is created for every test, so creating one app for all tests
        cls.app = create_app()

    def test_create_rapidos(self):
        with self.app.test_client() as client:
            found_rule = filter(lambda rule: rule.rule == '/api/rapidos/', self.app.url_map.iter_rules())
            self.assertEqual(1, len(list(found_rule)))

            expected_rapidos = {'name': 'Test Open Space', 'start': datetime(2021, 3, 2, 20).isoformat(),
                                'duration': 60,
                                'sessions': 2}

            with self.app.container.creation_service.override(CreationServiceMock('5678')):
                response = client.post('/api/rapidos/', json=expected_rapidos)
                self.assertEqual(201, response.status_code, response)
                expected_rapidos['id'] = '5678'
                self.assertEqual(expected_rapidos, response.json)

    def test_get_rapidos(self):
        with self.app.test_client() as client:
            expected_date = datetime(2021, 3, 2, 20)
            uuid_ = str(uuid.uuid4())
            expected_rapidos = {'name': 'Test Open Space', 'start': expected_date.isoformat(),
                                'id':uuid_,
                                'duration': 60,
                                'sessions': 2}

            service_mock = CreationServiceMock(uuid_)

            service_mock.create(expected_rapidos['name'], expected_date,
                                timedelta(minutes=expected_rapidos['duration']), expected_rapidos['sessions'])
            with self.app.container.creation_service.override(service_mock):
                response = client.get(f'/api/rapidos/{uuid_}')
                self.assertEqual(200, response.status_code, response)

                self.assertEqual(expected_rapidos, response.json)
