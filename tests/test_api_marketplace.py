import json
from unittest import TestCase

from rapidos.web import create_app


class TestApiMarketplace(TestCase):

    def test_get_marketplace_by_id(self):
        app = create_app()
        with app.test_client() as client:
            response = client.get(f'rapidos/api/marketplace/5')
            self.assertEqual(200, response.status_code)
            self.assertEqual([{
                "slot": "13:00",
                "topic": "Thema 1"
            }], json.loads(response.data))
