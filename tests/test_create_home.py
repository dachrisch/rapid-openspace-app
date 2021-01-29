from unittest import TestCase

from bs4 import BeautifulSoup

from rapidos.web import create_app
from rapidos.web.views import CreateForm
from tests.fixtures import OverridingContainer


class TestCreateHomeWeb(TestCase):

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
            self._has_input(soup, form.name.id, form.name.label.text)
            self._has_input(soup, form.count.id, form.count.label.text, _type='select')
            self._has_input(soup, form.length.id, form.length.label.text, _type='select')

    def test_create_os_uuid_created(self):
        app = create_app()
        app.container.override(OverridingContainer())
        app.container.creation_service().id = 5
        with app.test_client() as client:
            client.get('/rapidos/create', follow_redirects=False)

            form = CreateForm()
            response = client.post('/rapidos/create', data={form.name.id: 'test', form.count.id: 2, form.length.id: 2,
                                                            form.submit.id: form.submit.data,
                                                            form.csrf_token.id: form.csrf_token.current_token})
            self.assertEqual(302, response.status_code)
            self.assertEqual('http://localhost/rapidos/5/', response.location)

    def _has_input(self, soup, id, label_name, _type='input'):
        element = soup.find(id=id)
        self.assertEqual(_type, element.name)
        label = [i for i in element.previous_siblings][1]
        self.assertEqual(label_name, label.text)
