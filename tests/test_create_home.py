from unittest import TestCase

from bs4 import BeautifulSoup

from rapidos.web import create_app
from rapidos.web.forms import CreateForm
from tests.fixtures import OverridingContainer


class TestCreateRapidos(TestCase):

    def test_homepage(self):
        with create_app().test_client() as client:
            response = client.get('/rapidos/create', follow_redirects=False)
            self.assertEqual(200, response.status_code)
            self.assertIn(b'<h3>Willkommen zu deinem Open Space</h3>', response.data)

    def test_create_os_form_present(self):
        with create_app().test_client() as client:
            response = client.get('/rapidos/create', follow_redirects=False)
            self.assertEqual(200, response.status_code)
            soup = BeautifulSoup(response.data, features='lxml')
            form = CreateForm()
            self._has_input(soup, form.name_field.id, form.name_field.label.text)
            self._has_input(soup, form.sessions_field.id, form.sessions_field.label.text, _type='select')
            self._has_input(soup, form.duration_field.id, form.duration_field.label.text, _type='select')

    def test_create_os_uuid_created(self):
        app = create_app()
        app.container.override(OverridingContainer())
        app.container.creation_service().id = 5
        with app.test_client() as client:
            client.get('/rapidos/create', follow_redirects=False)

            form = CreateForm()
            response = client.post('/rapidos/create', data={form.name_field.id: 'test', form.sessions_field.id: 2,
                                                            form.duration_field.id: 2,
                                                            form.submit.id: form.submit.data,
                                                            form.csrf_token.id: form.csrf_token.current_token})
            self.assertEqual(302, response.status_code)
            self.assertEqual('http://localhost/rapidos/5/', response.location)

    def _has_input(self, soup, id, label_name, _type='input'):
        element = soup.find(id=id)
        self.assertEqual(_type, element.name)
        label = [i for i in element.previous_siblings][1]
        self.assertEqual(label_name, label.text)
