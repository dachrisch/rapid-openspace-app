from datetime import datetime, timedelta
from unittest import TestCase

from rapidos import RapidosService
from rapidos.web import create_app


class CreationServiceMock(RapidosService):
    def create(self, name: str, start: datetime, duration: timedelta, sessions: int):
        return '5678'


class TestRapidosApi(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # XXX: workaround, cause API lazy init is not working correctly
        # when app is created for every test, so creating one app for all tests
        cls.app = create_app()

    def test_create_rapidos(self):
        with self.app.test_client() as client:
            found_rule = filter(lambda rule: rule.rule == '/api/v1/rapidos', self.app.url_map.iter_rules())
            self.assertEqual(1, len(list(found_rule)))

            expected_rapidos = {'name': 'Test Open Space', 'start': datetime(2021, 3, 2, 20).isoformat(),
                                'duration': 60,
                                'sessions': 2}

            with self.app.container.creation_service.override(CreationServiceMock()):
                response = client.post('/api/v1/rapidos',
                                       json=expected_rapidos)
                self.assertEqual(201, response.status_code, response)

                expected_rapidos['id'] = '5678'
                self.assertEqual(expected_rapidos, response.json)
