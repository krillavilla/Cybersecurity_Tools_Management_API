import unittest
import json
import os
from app import create_app
from models import db, User, Tool
from unittest.mock import patch
from config import SQLiteTestConfig

# Mock tokens for testing purposes only
# These are fake JWT tokens with a structure similar to real tokens but with no valid signatures
# Format: header.payload.signature where each part is base64url encoded
# The signatures are explicitly marked as 'MOCK' to indicate these are not real tokens
# Each token has different permissions to test different roles

# Token for Tool Viewer role (read:tools permission only)
TOOL_VIEWER_TOKEN = 'eyJhbGciOiJNT0NLIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJuYW1lIjoiVG9vbCBWaWV3ZXIiLCJpYXQiOjEyMzQ1Njc4OTAsInBlcm1pc3Npb25zIjpbInJlYWQ6dG9vbHMiXX0.MOCK_SIGNATURE_FOR_TESTING_ONLY'

# Token for Tool Editor role (read:tools and update:tools permissions)
TOOL_EDITOR_TOKEN = 'eyJhbGciOiJNT0NLIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJuYW1lIjoiVG9vbCBFZGl0b3IiLCJpYXQiOjEyMzQ1Njc4OTAsInBlcm1pc3Npb25zIjpbInJlYWQ6dG9vbHMiLCJ1cGRhdGU6dG9vbHMiXX0.MOCK_SIGNATURE_FOR_TESTING_ONLY'

# Token for Tool Admin role (all permissions)
TOOL_ADMIN_TOKEN = 'eyJhbGciOiJNT0NLIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0LXVzZXItaWQiLCJuYW1lIjoiVG9vbCBBZG1pbiIsImlhdCI6MTIzNDU2Nzg5MCwicGVybWlzc2lvbnMiOlsicmVhZDp0b29scyIsImNyZWF0ZTp0b29scyIsInVwZGF0ZTp0b29scyIsImRlbGV0ZTp0b29scyJdfQ.MOCK_SIGNATURE_FOR_TESTING_ONLY'

# Mock Auth0 verification
def mock_verify_decode_jwt(token):
    if token == TOOL_VIEWER_TOKEN:
        return {'permissions': ['read:tools']}
    elif token == TOOL_EDITOR_TOKEN:
        return {'permissions': ['read:tools', 'update:tools']}
    elif token == TOOL_ADMIN_TOKEN:
        return {'permissions': ['read:tools', 'create:tools', 'update:tools', 'delete:tools']}
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
        self.sample_user = User(username="Test User", email="testuser@example.com")
        db.session.add(self.sample_user)
        db.session.commit()

        # Create a sample tool associated with the sample user
        self.sample_tool = Tool(name="Test Tool", description="A test tool.", user_id=self.sample_user.id)
        db.session.add(self.sample_tool)
        db.session.commit()

        # Set up tokens for different roles
        self.viewer_auth_header = {'Authorization': f'Bearer {TOOL_VIEWER_TOKEN}'}
        self.editor_auth_header = {'Authorization': f'Bearer {TOOL_EDITOR_TOKEN}'}
        self.admin_auth_header = {'Authorization': f'Bearer {TOOL_ADMIN_TOKEN}'}

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

    # Tests for success behavior
    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_get_tools(self, mock_verify_jwt):
        """Test getting all tools"""
        response = self.client.get('/api/tools', headers=self.viewer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['tools']) > 0)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_get_tool(self, mock_verify_jwt):
        """Test getting a specific tool"""
        response = self.client.get(f'/api/tools/{self.sample_tool.id}', headers=self.viewer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['tool']['id'], self.sample_tool.id)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_create_tool(self, mock_verify_jwt):
        """Test creating a new tool"""
        new_tool = {
            'name': 'New Test Tool',
            'description': 'A new test tool',
            'user_id': self.sample_user.id
        }

        response = self.client.post('/api/tools', json=new_tool, headers=self.admin_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['tool']['name'], 'New Test Tool')

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_update_tool(self, mock_verify_jwt):
        """Test updating a tool"""
        updated_tool = {
            'name': 'Updated Test Tool'
        }

        response = self.client.patch(f'/api/tools/{self.sample_tool.id}', json=updated_tool, headers=self.editor_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['tool']['name'], 'Updated Test Tool')

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_delete_tool(self, mock_verify_jwt):
        """Test deleting a tool"""
        response = self.client.delete(f'/api/tools/{self.sample_tool.id}', headers=self.admin_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], self.sample_tool.id)

    # Tests for error behavior
    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_404_get_nonexistent_tool(self, mock_verify_jwt):
        """Test getting a nonexistent tool"""
        response = self.client.get('/api/tools/9999', headers=self.viewer_auth_header)

        self.assertEqual(response.status_code, 404)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_422_create_tool_bad_request(self, mock_verify_jwt):
        """Test creating a tool with bad request data (expects 422 Unprocessable Entity)"""
        response = self.client.post('/api/tools', json={}, headers=self.admin_auth_header)

        self.assertEqual(response.status_code, 422)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_404_update_nonexistent_tool(self, mock_verify_jwt):
        """Test updating a nonexistent tool"""
        updated_tool = {
            'name': 'Updated Nonexistent Tool'
        }
        response = self.client.patch('/api/tools/9999', json=updated_tool, headers=self.editor_auth_header)

        self.assertEqual(response.status_code, 404)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_404_delete_nonexistent_tool(self, mock_verify_jwt):
        """Test deleting a nonexistent tool"""
        response = self.client.delete('/api/tools/9999', headers=self.admin_auth_header)

        self.assertEqual(response.status_code, 404)

    # Tests for RBAC
    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_viewer_can_read(self, mock_verify_jwt):
        """Test that a viewer can read tools"""
        response = self.client.get('/api/tools', headers=self.viewer_auth_header)

        self.assertEqual(response.status_code, 200)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_viewer_cannot_create(self, mock_verify_jwt):
        """Test that a viewer cannot create tools"""
        new_tool = {
            'name': 'New Test Tool',
            'description': 'A new test tool',
            'user_id': self.sample_user.id
        }

        response = self.client.post('/api/tools', json=new_tool, headers=self.viewer_auth_header)

        self.assertEqual(response.status_code, 403)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_editor_can_update(self, mock_verify_jwt):
        """Test that an editor can update tools"""
        updated_tool = {
            'name': 'Updated by Editor'
        }

        response = self.client.patch(f'/api/tools/{self.sample_tool.id}', json=updated_tool, headers=self.editor_auth_header)

        self.assertEqual(response.status_code, 200)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_editor_cannot_delete(self, mock_verify_jwt):
        """Test that an editor cannot delete tools"""
        response = self.client.delete(f'/api/tools/{self.sample_tool.id}', headers=self.editor_auth_header)

        self.assertEqual(response.status_code, 403)

    @patch('auth.verify_decode_jwt', side_effect=mock_verify_decode_jwt)
    def test_admin_full_access(self, mock_verify_jwt):
        """Test that an admin has full access"""
        # Test read
        response = self.client.get('/api/tools', headers=self.admin_auth_header)
        self.assertEqual(response.status_code, 200)

        # Test create
        new_tool = {
            'name': 'Admin Tool',
            'description': 'Created by admin',
            'user_id': self.sample_user.id
        }
        response = self.client.post('/api/tools', json=new_tool, headers=self.admin_auth_header)
        self.assertEqual(response.status_code, 201)

        # Get the created tool's ID
        data = json.loads(response.data)
        tool_id = data['tool']['id']

        # Test update
        updated_tool = {
            'name': 'Updated Admin Tool'
        }
        response = self.client.patch(f'/api/tools/{tool_id}', json=updated_tool, headers=self.admin_auth_header)
        self.assertEqual(response.status_code, 200)

        # Test delete
        response = self.client.delete(f'/api/tools/{tool_id}', headers=self.admin_auth_header)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
