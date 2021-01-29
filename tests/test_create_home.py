from unittest import TestCase

from rapidos.web import create_app


class TestCreateHomeWeb(TestCase):

    def setUp(self):
        self.test_client = create_app().test_client()

    def test_homepage(self):
        response = self.test_client.get('/rapidos/create/', follow_redirects=False)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'<h1>Hello Open Space World</h1>', response.data)
