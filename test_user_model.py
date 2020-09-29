"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.email, "test@test.com")

        self.assertEqual(User.authenticate(
            'testuser', 'HASHED_PASSWORD'), u)
        self.assertEqual(User.authenticate(
            'testuser', 'WRONG_PASSWORD'), False)

    def test_user_create_failure(self):
        """does the user model signup method fail correctly?"""

        u1 = User(
            email="test@test.com",
            username="",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        self.assertEqual(u1, None)

    def test_user_duplicate_failure(self):
        """does a non-unique entry fail?"""

        u1 = User(
            email="u1@test.com",
            username="u1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="u2@test.com",
            username="u1",
            password="OTHER_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u2, None)

    def test_user_following(self):
        """can we correctly determine followers?"""

        u1 = User(
            email="u1@test.com",
            username="u1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="u2@test.com",
            username="u2",
            password="OTHER_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        do_login(u1)

        with app.test_client() as client:
            resp = client.post(
                f'/users/follow/{u2.id}'
            )

            self.assertEqual(u1.is_followed_by(u2), True)
            self.assertEqual(u2.is_followed_by(u1), False)
            self.assertEqual(u2.is_following(u1), True)
            self.assertEqual(u1.is_following(u2), False)
