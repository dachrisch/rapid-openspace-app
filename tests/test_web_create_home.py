from datetime import datetime
from unittest import TestCase

from lxml import html

from rapidos.web import create_app
from rapidos.web.forms import CreateForm


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
            tree = html.document_fromstring(response.data.decode("utf-8"))
            form = CreateForm()
            self._has_input(tree, form.name_field.id, form.name_field.label.text)
            self._has_input(tree, form.sessions_field.id, form.sessions_field.label.text, _type='select')
            self._has_input(tree, form.duration_field.id, form.duration_field.label.text, _type='select')

    def test_create_os_uuid_created(self):
        app = create_app()
        with app.test_client() as client:
            client.get('/rapidos/create', follow_redirects=False)

            form = CreateForm()
            response = client.post('/rapidos/create', data={form.name_field.id: 'test', form.sessions_field.id: 2,
                                                            form.duration_field.id: 2,
                                                            form.submit.id: form.submit.data,
                                                            form.start_field.id: datetime.now().strftime(
                                                                '%d.%m.%Y - %H:%M'),
                                                            form.csrf_token.id: form.csrf_token.current_token})
            self.assertEqual(302, response.status_code)
            self.assertRegex(response.location, 'http://localhost/rapidos/\w+-\w+-\w+-\w+')

    def _has_input(self, tree, id, expected_label_text, _type='input'):
        element = tree.xpath(f'//{_type}[@id="{id}"]')
        self.assertIsNotNone(element)
        label_text = tree.xpath(f'//label[@for="{id}"]/text()')
        self.assertEqual(1, len(label_text))
        self.assertEqual(expected_label_text, label_text[0])
