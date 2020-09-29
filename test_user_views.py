from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class UserViewsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
