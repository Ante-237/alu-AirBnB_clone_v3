#!/usr/bin/python3
""" test case """
import unittest
from models.city import City
from models.state import State
from models.engine import db_storage
from models.amenity import Amenity
from models.user import User
from models import storage
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if fs")
class TestGet(unittest.TestCase):
    """ test of get method """

    def setUp(self):
        self.storage = db_storage.DBStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()
        self.new_city = City(name="San Francisco", state_id=self.new_state.id)
        self.new_city.save()

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.delete(self.new_city)
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_get_existing_object(self):
        """Test get() with an object that exists"""
        obj = self.storage.get(City, self.new_city.id)
        self.assertEqual(obj.id, self.new_city.id)

    def test_get_nonexistent_object(self):
        """Test get() with an object that does not exist"""
        obj = self.storage.get(State, "nonexistent")
        self.assertIsNone(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCount(unittest.TestCase):
    """Tests the count() method of the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = db_storage.DBStorage()
        self.storage.reload()
        self.new_state1 = State(name="California")
        self.new_state2 = State(name="New York")
        self.new_state3 = State(name="Texas")
        self.new_state1.save()
        self.new_state2.save()
        self.new_state3.save()

    def tearDown(self):
        """Tear down"""
        self.storage.delete(self.new_state1)
        self.storage.delete(self.new_state2)
        self.storage.delete(self.new_state3)
        self.storage.save()
        self.storage.close()

    def test_count_all_objects(self):
        """Test count() with no arguments"""
        count = self.storage.count()
        self.assertEqual(count, 3)

    def test_count_some_objects(self):
        """Test count() with a class argument"""
        count = self.storage.count(State)
        self.assertEqual(count, 3)

    def test_count_nonexistent_class(self):
        """Test count() with a nonexistent class argument"""
        count = self.storage.count(Amenity)
        self.assertEqual(count, 0)

    def test_get_db(self):
        """ Tests method get test"""
        dic = {"name": "California"}
        instance = State(**dic)
        self.storage.new(instance)
        self.storage.save()
        get_instance = self.storage.get(State, instance.id)
        self.assertEqual(get_instance, instance)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageGet(unittest.TestCase):
    """get test"""

    def setUp(self):
        """Set up"""
        self.storage = db_storage.DBStorage()
        self.storage.reload()
        self.new_user1 = User(email="user@example.com", password="pass")
        self.new_user2 = User(email="user0@example.com", password="nothing")
        self.new_user1.save()
        self.new_user2.save()

    def tearDown(self):
        """Tear down"""
        self.storage.delete(self.new_user1)
        self.storage.delete(self.new_user2)
        self.storage.save()
        self.storage.close()

    def test_get_existing_user(self):
        """Test get() with user"""
        obj = self.storage.get(User, self.new_user1.id)
        self.assertEqual(obj.id, self.new_user1.id)

    def test_get_nonexistent_user(self):
        """Test get() none User"""
        obj = self.storage.get(User, "nonexistent")
        self.assertIsNone(obj)


