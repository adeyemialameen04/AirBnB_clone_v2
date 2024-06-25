import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


class TestConsole(unittest.TestCase):
    """Test cases for the HBNBCommand class"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.console = HBNBCommand()

    def setUp(self):
        """Set up each test"""
        self.resetStorage()
        self.obj = BaseModel()
        self.obj.save()

    def tearDown(self):
        """Clean up after each test"""
        self.resetStorage()

    def resetStorage(self):
        """Reset storage"""
        storage.all().clear()
        storage.save()

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertIs(self.console.onecmd("quit"), True)

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            output = f.getvalue().strip()
        self.assertTrue(len(output) > 0)  # Check if an instance ID is printed

    def test_show(self):
        """Test show command"""
        obj_id = self.obj.id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show BaseModel {obj_id}")
            output = f.getvalue().strip()
        self.assertIn(str(self.obj), output)

    def test_all(self):
        """Test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
        self.assertIn("[BaseModel]", output)

    def test_update(self):
        """Test update command"""
        obj_id = self.obj.id
        attr_name = "name"
        attr_value = "Test Model"
        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"update BaseModel {obj_id} {
                                attr_name} '{attr_value}'")
        self.assertEqual(getattr(self.obj, attr_name), attr_value)

    def test_default(self):
        """Test default command"""
        obj_id = self.obj.id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"BaseModel.show('{obj_id}')")
            output = f.getvalue().strip()
        self.assertIn(str(self.obj), output)


if __name__ == '__main__':
    unittest.main()
