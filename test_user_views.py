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

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_delete_message(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
