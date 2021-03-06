import shlex
import time
from datetime import datetime
from subprocess import Popen, STDOUT, PIPE
from unittest import TestCase

import requests
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from rapidos.web import create_app


class TestCreateRapidosIntegration(TestCase):
    def setUp(self) -> None:
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 3)

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
        created_rapidos = requests.post(f'{self.base_url}/api/rapidos/',
                                        json={'name': 'Test Open Space', 'start': datetime(2021, 3, 2, 20).isoformat(),
                                              'duration': 60,
                                              'sessions': 2})

        self.assertEqual(201, created_rapidos.status_code)
        rapidos_id = created_rapidos.json()['id']

        self.driver.get(f'{self.base_url}/rapidos/create')
        self.driver.get(f'{self.base_url}/rapidos/{rapidos_id}')
        self.driver.find_element_by_id('session_location').send_keys('Test Location')
        self.driver.find_element_by_id('add_location_button').click()

        self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//th[@class="location"]')))

        rapidos_locations = requests.get(f'{self.base_url}/api/rapidos/{rapidos_id}/locations')
        self.assertEqual(200, rapidos_locations.status_code)
        location_id = rapidos_locations.json()[0]['id']

        location_panel_text = self.driver.find_element_by_id(f'loc_{location_id}').text.split('\n')
        self.assertEqual('Test Location', location_panel_text[0])

    def test_remove_location(self):
        created_rapidos = requests.post(f'{self.base_url}/api/rapidos/',
                                        json={'name': 'Test Open Space', 'start': datetime(2021, 3, 2, 20).isoformat(),
                                              'duration': 60,
                                              'sessions': 2})

        self.assertEqual(201, created_rapidos.status_code)
        rapidos_id = created_rapidos.json()['id']

        self.driver.get(f'{self.base_url}/rapidos/create')
        self.driver.get(f'{self.base_url}/rapidos/{rapidos_id}')
        self.driver.find_element_by_id('session_location').send_keys('Test Location')
        self.driver.find_element_by_id('add_location_button').click()

        rapidos_locations = requests.get(f'{self.base_url}/api/rapidos/{rapidos_id}/locations')
        self.assertEqual(200, rapidos_locations.status_code)
        location_id = rapidos_locations.json()[0]['id']

        self.driver.find_element_by_id(f'close_loc_{location_id}').click()

        self.wait.until(expected_conditions.invisibility_of_element_located((By.ID, f'loc_{location_id}')))

        rapidos_locations = requests.get(f'{self.base_url}/api/rapidos/{rapidos_id}/locations')
        self.assertEqual(200, rapidos_locations.status_code)
        self.assertEqual(0, len(rapidos_locations.json()))
