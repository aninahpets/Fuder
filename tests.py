import unittest

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