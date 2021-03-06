import uuid
from datetime import datetime, timedelta
from unittest import TestCase

from rapidos.web import create_app
from tests.fixtures import CreationServiceMock


class RapidosApiTestBase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # XXX: workaround, cause API lazy init is not working correctly
        # when app is created for every test, so creating one app for all tests
        cls.app = create_app()


class TestRapidosApi(RapidosApiTestBase):

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
                                'id': uuid_,
                                'duration': 60,
                                'sessions': 2}

            service_mock = CreationServiceMock(uuid_)

            service_mock.create(expected_rapidos['name'], expected_date,
                                timedelta(minutes=expected_rapidos['duration']), expected_rapidos['sessions'])
            with self.app.container.creation_service.override(service_mock):
                response = client.get(f'/api/rapidos/{uuid_}')
                self.assertEqual(200, response.status_code, response)

                self.assertEqual(expected_rapidos, response.json)


class TestSessionLocationApi(RapidosApiTestBase):

    def test_create_location(self):
        with self.app.test_client() as client:
            uuid_ = str(uuid.uuid4())
            service_mock = CreationServiceMock(uuid_)

            service_mock.create('Test Rapidos', datetime(2021, 4, 1), timedelta(minutes=30), 1)
            with self.app.container.creation_service.override(service_mock):
                response = client.post(f'/api/rapidos/{uuid_}/locations', json={'name': 'test location'})
                self.assertEqual(201, response.status_code, response)
                self.assertEqual({'id': uuid_, 'name': 'test location'}, response.json)

    def test_get_locations(self):
        with self.app.test_client() as client:
            uuid_ = str(uuid.uuid4())
            service_mock = CreationServiceMock(uuid_)
            service_mock.create('Test Rapidos', datetime(2021, 4, 1), timedelta(minutes=30), 1)
            session_location = service_mock.add_session_location('Test Location').to(uuid_)
            with self.app.container.creation_service.override(service_mock):
                response = client.get(f'/api/rapidos/{uuid_}/locations')
                self.assertEqual(200, response.status_code, response)
                self.assertEqual([{'id': session_location.id, 'name': session_location.name}], response.json)

    def test_get_location(self):
        with self.app.test_client() as client:
            uuid_ = str(uuid.uuid4())
            service_mock = CreationServiceMock(uuid_)
            service_mock.create('Test Rapidos', datetime(2021, 4, 1), timedelta(minutes=30), 1)
            session_location = service_mock.add_session_location('Test Location').to(uuid_)
            with self.app.container.creation_service.override(service_mock):
                response = client.get(f'/api/rapidos/{uuid_}/locations/{session_location.id}')
                self.assertEqual(200, response.status_code, response)
                self.assertEqual({'id': session_location.id, 'name': session_location.name}, response.json)

    def test_remove_location(self):
        with self.app.test_client() as client:
            uuid_ = str(uuid.uuid4())
            service_mock = CreationServiceMock(uuid_)
            service_mock.create('Test Rapidos', datetime(2021, 4, 1), timedelta(minutes=30), 1)
            session_location = service_mock.add_session_location('Test Location').to(uuid_)
            with self.app.container.creation_service.override(service_mock):
                response = client.delete(f'/api/rapidos/{uuid_}/locations/{session_location.id}')
                self.assertEqual(200, response.status_code, response)

                self.assertEqual(set(), service_mock.get_session_locations().of(uuid_))
