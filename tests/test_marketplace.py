import uuid
from datetime import timedelta, datetime
from unittest import TestCase

from rapidos.web import create_app
from tests.fixtures import OverridingContainer


class TestMarketplace(TestCase):

    def test_marketplace_uri(self):
        app = create_app()
        app.container.override(OverridingContainer())
        app.container.creation_service().id = uuid.uuid4()
        uuid_ = app.container.creation_service().create('test os', datetime.now(), timedelta(minutes=30), 2)
        with app.test_client() as client:
            response = client.get(f'/rapidos/{uuid_}/', follow_redirects=False)

            self.assertEqual(200, response.status_code)
            self.assertIn(b'<h3>Willkommen zum Open Space', response.data)
            self.assertIn(b'<i>test os</i>', response.data)
