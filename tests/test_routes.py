import unittest
from app import app, db
from app.models import Tool


class ToolTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def test_get_tools(self):
        response = self.app.get('/tools')
        self.assertEqual(response.status_code, 200)

    def test_create_tool(self):
        response = self.app.post('/tools', json={
            'name': 'New Tool',
            'category': 'Malware Analysis',
            'platform': 'Windows',
            'license': 'GPL'
        })
        self.assertEqual(response.status_code, 201)
