import shlex
import time
from datetime import datetime
from subprocess import Popen, STDOUT, PIPE
from unittest import TestCase

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from requests.exceptions import ConnectionError
from rapidos.web import create_app


class TestCreateRapidosIntegration(TestCase):
    def setUp(self) -> None:
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.app = create_app()

        self.base_url = 'http://127.0.0.1:5000'

        self.server = Popen(shlex.split('python -m app'), stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        for tries in range(10):
            time.sleep(.1 * tries)
            try:
                response = requests.get(f'{self.base_url}/ping')
                if 200 == response.status_code:
                    break
            except ConnectionError:
                time.sleep(1)

    def tearDown(self) -> None:
        requests.get(f'{self.base_url}/shutdown')
        self.server.wait(timeout=5)
        self.server.terminate()

    def test_create_single_rapidos(self):
        self.driver.get(f'{self.base_url}/rapidos/create')
        main_div = self.driver.find_element_by_xpath('//main/h3')
        self.assertEqual('Willkommen zu deinem Open Space', main_div.text)

        self.driver.find_element_by_id('name_field').send_keys('Test Name')
        self.driver.find_element_by_id('start_field').send_keys('12.04.2021 - 09:45')
        Select(self.driver.find_element_by_id('sessions_field')).select_by_visible_text('1')
        Select(self.driver.find_element_by_id('duration_field')).select_by_visible_text('30 Minuten')

        self.driver.find_element_by_id('submit').click()

        rapidos_id = self.driver.current_url.split('/')[-1]
        self._is_uuid_format(rapidos_id)

    def _is_uuid_format(self, text):
        self.assertRegex(text, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    def test_create_a_location(self):
        self.driver.get(f'{self.base_url}/rapidos/create')
        response = requests.post(f'{self.base_url}/api/rapidos/',
                                 json={'name': 'Test Open Space', 'start': datetime(2021, 3, 2, 20).isoformat(),
                                       'duration': 60,
                                       'sessions': 2})

        self.assertEqual(201, response.status_code)
        rapidos_id = response.json()['id']

        self.driver.get(f'{self.base_url}/rapidos/{rapidos_id}')
        self.driver.find_element_by_id('session_location').send_keys('Test Location')
        self.driver.find_element_by_id('add_session_button').click()

        location_panel_text = self.driver.find_element_by_id('Test LocationPanel').text.split('\n')
        self.assertEqual('Location #Test Location', location_panel_text[0])
        self._is_uuid_format(location_panel_text[1])
