import unittest
from app import create_app
from models import db, User, Tool
from flask_jwt_extended import create_access_token

class CapstoneTestCase(unittest.TestCase):
    """
    Test case for the Cybersecurity Tools Management API.
    """

    def setUp(self):
        """
        Set up the test client and initialize the database.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.create_all()

        # Create a sample user
        sample_user = User(username="Test User", email="testuser@example.com")
        db.session.add(sample_user)
        db.session.commit()

        # Create a sample tool associated with the sample user
        sample_tool = Tool(name="Test Tool", description="A test tool.", user_id=sample_user.id)
        db.session.add(sample_tool)
        db.session.commit()

        # Generate a JWT token for the sample user with the required permissions
        self.token = create_access_token(identity=sample_user.id, additional_claims={"permissions": ["read:tools"]})
        print(f"Generated Token: {self.token}")

    def tearDown(self):
        """
        Tear down the test client and drop the database.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_home(self):
        """
        Test the home endpoint to ensure it returns the correct response.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Cybersecurity Tools Management API!", response.data)

if __name__ == '__main__':
    unittest.main()