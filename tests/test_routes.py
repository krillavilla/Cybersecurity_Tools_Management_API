import unittest
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app import db
from models import Tool  # Adjust the import based on your actual model name

class APITestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app('testing')  # Use testing configuration
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # Create tables
        self.populate_test_data()
        self.token = self.generate_token()

    def tearDown(self):
        """Clean up the database and context."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_test_data(self):
        """Insert mock data into the database."""
        tool = Tool(name="Existing Tool", description="A tool for testing")
        db.session.add(tool)
        db.session.commit()

    def generate_token(self):
        """Generate a valid JWT token for testing."""
        # Implement token generation logic
        # Example: return "your_actual_valid_token"
        return "mock_token_for_testing"

    def test_get_tools(self):
        """Test retrieving tools."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get('/tools', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Existing Tool", response.data)

    def test_create_tool(self):
        """Test creating a tool."""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"name": "New Tool", "description": "Tool Description"}
        response = self.client.post('/tools', headers=headers, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"New Tool", response.data)

    def test_update_tool(self):
        """Test updating a tool."""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"name": "Updated Tool Name", "description": "Updated Tool Description"}
        response = self.client.patch('/tools/1', headers=headers, data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Updated Tool Name", response.data)

    def test_delete_tool(self):
        """Test deleting a tool."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete('/tools/1', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()