import unittest
from selenium import webdriver

from server import app
from model import db, connect_to_db

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///project"

class HomepageTests(unittest.TestCase):
    """Tests for non-registered users."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_not_registered_yet(self):
        result = self.client.get('/')
        self.assertIn('registered?')

    def test_registered(self):
        result = self.client.get('/')
        self.assertNotIn('Where are you?')


class SeleniumTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_login_title(self):
        self.browser.get('http://localhost:5000/login')
        self.assertEqual(self.browser.title, 'Login')

    def test_homepage_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'Homepage')


def _mock_get_start_coordinates(address):
    latitude = 37.8044
    longitude = 122.2711
    return latitude, longitude

import server
server.get_start_coordinates = _mock_get_start_coordinates


if __name__ == "__main__":
    unittest.main()