import unittest
import pdb
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
        self.assertNotIn('want to do?', result.data)

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

    def test_registered_homepage(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertIn('want to do', result.data)
        
    def test_registered_not_redirected_to_login(self):
        result = self.client.get('/', follow_redirects=True)
        self.assertNotIn('registered?', result.data)

    def test_registered_redirected_to_homepage(self):
        result = self.client.get('/login', follow_redirects=True)
        self.assertIn('want to do', result.data)


class SeleniumTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_login_title(self):
        self.browser.get('http://localhost:5000/login')
        self.assertEqual(self.browser.title, 'Login')

    def test_user_flow_and_submission(self):
        self.browser.get('http://localhost:5000/')

        user = self.browser.find_element_by_id('field-email')
        user.send_keys('test@test.com')

        pw = self.browser.find_element_by_id('field-password')
        pw.send_keys('password')

        login_btn = self.browser.find_element_by_id('field-login-button')
        login_btn.click()

        result = self.assertEqual(self.browser.title, 'Fuder')

        eat_btn = self.browser.find_element_by_id('restaurant-button')
        eat_btn.click()
        
        select = self.browser.find_element_by_id('venue-options')
        for option in select.find_elements_by_tag_name('option'):
            if option.text == 'Surprise Me!':
                option.click()

        address = self.browser.find_element_by_id('field-user-address')
        address.send_keys('123 Main St, San Francisco, CA 94105')

        submit_btn = self.browser.find_element_by_id('uber-auth-button')
        submit_btn.click()

        assert 'Forgot Password' in self.browser.find_element_by_class_name('forgot-password').text


def _mock_get_start_coordinates(address):
    latitude = 37.8044
    longitude = -122.2711
    return latitude, longitude

import server
server.get_start_coordinates = _mock_get_start_coordinates


if __name__ == "__main__":  # pragma: no cover
    unittest.main()