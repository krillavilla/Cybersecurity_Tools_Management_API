import unittest
from app import app, db
from app.models import Tool


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_tools(self):
        response = self.app.get('/tools')
        self.assertEqual(response.status_code, 200)

    def test_create_tool(self):
        response = self.app.post('/tools', json={
            'name': 'New Tool',
            'category': 'Category',
            'platform': 'Platform',
            'license': 'License'
        })
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
