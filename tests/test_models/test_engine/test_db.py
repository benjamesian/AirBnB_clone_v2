#!/usr/bin/python3
"""test for database storage"""
import unittest
import pep8
import MySQLdb
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "using file, so skip db tests")
class TestDBStorage(unittest.TestCase):
    '''this will test the Database Storage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.connection = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                               user=os.getenv('HBNB_MYSQL_USER'),
                               passwd=os.getenv('HBNB_MYSQL_PWD'),
                               db=os.getenv('HBNB_MYSQL_DB'),
                               charset="utf8")

        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = DBStorage()

    @classmethod
    def tearDownClass(cls):
        """at the end of the test this will tear it down"""
        del cls.user
        cls.connection.close()

    def setUp(self):
        """set up"""
        self.cursor = self.connection.cursor()

    def tearDown(self):
        """teardown"""
        self.cursor.close()
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_DBStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        self.cursor.execute("SELECT * FROM states ORDER BY id ASC")
        query_rows = self.cursor.fetchall()
        for row in query_rows:
            print(row)

        storage = DBStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._DBStorage__objects)

    def test_new(self):
        """test when new is created"""
        storage = DBStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_save(self):
        """test saving items to the database"""
        pass

    def test_reload_DBStorage(self):
        """
        tests reload
        """
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)


if __name__ == "__main__":
    unittest.main()
