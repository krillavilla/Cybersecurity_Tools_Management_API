import unittest
from app import create_app, db


class TestAppSetup(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Assuming you have a 'testing' config
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Set up the database before each test

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Clean up the database after each test

    def test_app_exists(self):
        self.assertIsNotNone(self.app)


if __name__ == "__main__":
    unittest.main()
