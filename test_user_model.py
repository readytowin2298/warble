"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

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

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User.query.first()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_is_following(self):
        u = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u)
        db.session.commit()
        users = User.query.all()
        u1 = users[0]
        u2 = users[1]

        self.assertEqual(2, len(users))
        self.assertFalse(u2.is_following(u1))

        
        f = Follows(user_being_followed_id=u1.id, user_following_id=u2.id)
        db.session.add(f)
        db.session.commit()
        self.assertTrue(u2.is_following(u1))

    def test_user_is_followed_by(self):
        u = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u)
        db.session.commit()
        users = User.query.all()
        u1 = users[0]
        u2 = users[1]
        
        
        self.assertEqual(2, len(users))
        self.assertFalse(u2.is_followed_by(u1))

        f = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(f)
        db.session.commit()
        self.assertTrue(u2.is_followed_by(u1))

    def test_create_and_auth(self):
        user = User.signup(username='test', email='imtired@beds.com', password='supersecure',
                    image_url='somerandopic.com/jpeg')
        db.session.commit()
        users = User.query.all()

        self.assertEqual(2, len(users))
        self.assertTrue(User.authenticate(username=user.username, password='supersecure'))
        self.assertFalse(User.authenticate(username=user.username, password='lol'))

