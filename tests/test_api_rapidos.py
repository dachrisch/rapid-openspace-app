import json
from unittest import TestCase

from rapidos.web import create_app


class TestRapidosApi(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # XXX: workaround, cause API lazy init is not working correctly
        # when app is created for every test, so creating one app for all tests
        cls.app = create_app()

    def test_rapidos_api_post_available(self):
        with self.app.test_client() as client:
            found_rule = filter(lambda rule: rule.rule == '/api/v1/rapidos', self.app.url_map.iter_rules())
            self.assertEqual(1, len(list(found_rule)), list(self.app.url_map.iter_rules()))
            response = client.post('/api/v1/rapidos', json={'name': 'Test Open Space'})
            self.assertEqual(201, response.status_code)

    def test_create_rapidos(self):
        with self.app.test_client() as client:
            found_rule = filter(lambda rule: rule.rule == '/api/v1/rapidos', self.app.url_map.iter_rules())
            self.assertEqual(1, len(list(found_rule)))

            response = client.post('/api/v1/rapidos', json={'name': 'Test Open Space'})
            self.assertEqual(201, response.status_code)
