import unittest
from datetime import datetime, timedelta

from rapidos import RapidosService
from tests.fixtures import MockIdGenerator


class TestRapidosService(unittest.TestCase):

    def test_create_rapidos(self):
        rapidos_service = RapidosService(MockIdGenerator('123'))
        rapidos = rapidos_service.create('Test', datetime(2021, 1, 1), timedelta(minutes=30), 1)
        self.assertEqual('Test', rapidos.name)
        self.assertEqual('123', rapidos.id)

    def test_find_rapidos(self):
        rapidos_service = RapidosService(MockIdGenerator('123'))
        rapidos_service.create('Test', datetime(2021, 1, 1), timedelta(minutes=30), 1)
        rapidos = rapidos_service.get('123')
        self.assertEqual('Test', rapidos.name)
        self.assertEqual('123', rapidos.id)

    def test_add_session_location(self):
        rapidos_service = RapidosService(MockIdGenerator('123'))
        rapidos_service.create('Test', datetime(2021, 1, 1), timedelta(minutes=30), 1)
        location = rapidos_service.add_session_location('Test Location').to('123')
        self.assertEqual('123', location.id)
        self.assertEqual('Test Location', location.name)

    def test_get_session_locations(self):
        rapidos_service = RapidosService(MockIdGenerator('123'))
        rapidos_service.create('Test', datetime(2021, 1, 1), timedelta(minutes=30), 1)
        rapidos_service.add_session_location('Test Location').to('123')

        locations = rapidos_service.get_session_locations().of('123')
        self.assertEqual(1, len(locations))
        location = locations.pop()
        self.assertEqual('123', location.id)
        self.assertEqual('Test Location', location.name)


    def test_delete_session_location(self):
        rapidos_service = RapidosService(MockIdGenerator('123'))
        rapidos_service.create('Test', datetime(2021, 1, 1), timedelta(minutes=30), 1)
        session_location = rapidos_service.add_session_location('Test Location').to('123')

        rapidos_service.remove_session_locations(session_location.id).of('123')

        locations = rapidos_service.get_session_locations().of('123')
        self.assertEqual(0, len(locations))
