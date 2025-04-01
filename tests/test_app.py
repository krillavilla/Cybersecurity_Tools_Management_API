import unittest
import json
from app import create_app
from models import db, User, Tool
from unittest.mock import patch
from config import SQLiteTestConfig

# Mock tokens for testing purposes only
# This is a fake JWT token with a structure similar to real tokens but with no valid signature
# Format: header.payload.signature where each part is base64url encoded
# The signature is explicitly marked as 'MOCK' to indicate it's not a real token
TOOL_VIEWER_TOKEN = 'eyJhbGciOiJNT0NLIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJuYW1lIjoiVG9vbCBWaWV3ZXIiLCJpYXQiOjEyMzQ1Njc4OTAsInBlcm1pc3Npb25zIjpbInJlYWQ6dG9vbHMiXX0.MOCK_SIGNATURE_FOR_TESTING_ONLY'

# Mock Auth0 verification
def mock_verify_decode_jwt(token):
    if token == TOOL_VIEWER_TOKEN:
        return {'permissions': ['read:tools']}
    else:
        raise Exception('Invalid token')

class CapstoneTestCase(unittest.TestCase):
    """
    Test case for the Cybersecurity Tools Management API.
    """

    def setUp(self):
        """
        Set up the test client and initialize the database.
        """
        # Create the app with SQLiteTestConfig to use an in-memory database
        self.app = create_app(SQLiteTestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create all tables in the in-memory database
        db.create_all()

        # Create a sample user
        sample_user = User(username="Test User", email="testuser@example.com")
        db.session.add(sample_user)
        db.session.commit()

        # Create a sample tool associated with the sample user
        sample_tool = Tool(name="Test Tool", description="A test tool.", user_id=sample_user.id)
        db.session.add(sample_tool)
        db.session.commit()

        # Set up token for testing
        self.token = TOOL_VIEWER_TOKEN
        self.auth_header = {'Authorization': f'Bearer {self.token}'}

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

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_get_tools(self, mock_verify_jwt):
        """Test getting all tools"""
        response = self.client.get('/api/tools', headers=self.auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['tools']) > 0)

if __name__ == '__main__':
    unittest.main()
