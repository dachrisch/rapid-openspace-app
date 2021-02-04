import json
from unittest import TestCase

from rapidos.web import create_app


class TestRapidosApi(TestCase):

    def test_create_rapidos_via_rest(self):
        app = create_app()
        with app.test_client() as client:
            found_rule = filter(lambda rule: rule.rule == '/api/rapidos/', app.url_map.iter_rules())
            self.assertIsNotNone(found_rule)
            response = client.post('/api/rapidos/', json={'name': 'Test Open Space'})
            self.assertEqual(201, response.status_code)
