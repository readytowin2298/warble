import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app


db.create_all()

class MessageModelTestCase(TestCase):