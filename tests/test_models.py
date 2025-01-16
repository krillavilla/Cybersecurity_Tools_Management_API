import unittest
from app import db
from app.models import Tool


class TestDatabaseModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_tool(self):
        new_tool = Tool(name="Test Tool", description="Test Description")
        db.session.add(new_tool)
        db.session.commit()
        tool = Tool.query.first()
        self.assertEqual(tool.name, "Test Tool")
