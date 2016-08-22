import unittest
from selenium import webdriver

from server import app
from model import db, connect_to_db, example_data

class NotLoggedInTests(unittest.TestCase):
    """Tests for non-registered users."""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_user_without_session_redirects_homepage_to_login(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertIn('registered?', result.data)

    def test_user_without_session_does_not_provide_homepage(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertNotIn('Where are you?', result.data)

    def test_user_without_session_no_logout_option(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertNotIn('Log Out', result.data)


class LoggedInTests(unittest.TestCase):
    """Tests for registered users."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_not_registered_yet(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertNotIn('registered?', result.data)

    def test_registered(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertIn('ready', result.data)

    def test_visit_history(self):
        result = self.client.get('/history')
        self.assertIn('Where', result.data)


# class SeleniumTests(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_login_title(self):
#         self.browser.get('http://localhost:5000/login')
#         self.assertEqual(self.browser.title, 'Login')

    # def test_homepage_title(self):
    #     self.browser.get('http://localhost:5000')
    #     self.assertEqual(self.browser.title, 'Homepage')


def _mock_get_start_coordinates(address):
    latitude = 37.8044
    longitude = -122.2711
    return latitude, longitude

import server
server.get_start_coordinates = _mock_get_start_coordinates


if __name__ == "__main__":
    unittest.main()