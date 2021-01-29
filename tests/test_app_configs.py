import os
from unittest import TestCase

from rapidos.web import create_app


class TestAppConfigs(TestCase):

    def test_development(self):
        os.environ['FLASK_CONFIGURATION'] = 'default'
        app = create_app()
        self.assertTrue(app.config.get('DEBUG'))
        self.assertTrue(app.config.get('TESTING'))
