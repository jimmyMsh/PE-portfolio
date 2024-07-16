# test_db.py

import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):

    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', 
                                        email='john@example.com',
                                        content='Hello World, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe',
                                        email='jane@example.com',
                                        content='Hello World, I\'m Jane!')
        assert second_post.id == 2

        # Get timeline posts and assert that they are correct
        createdPosts = TimelinePost.select().order_by(TimelinePost.id)

        # Assert information from first post
        assert createdPosts[0].id == 1
        assert createdPosts[0].name == 'John Doe'
        assert createdPosts[0].email == 'john@example.com'
        assert createdPosts[0].content == 'Hello World, I\'m John!'

        # Assert information from second post
        assert createdPosts[1].id == 2
        assert createdPosts[1].name == 'Jane Doe'
        assert createdPosts[1].email == 'jane@example.com'
        assert createdPosts[1].content == 'Hello World, I\'m Jane!'