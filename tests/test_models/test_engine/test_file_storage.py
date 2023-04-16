#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.user import User
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
import os


class TestFileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage.all().keys():
            del_list.append(key)
        for key in del_list:
            del storage.all()[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except:
            pass

    @unittest.skip(" not right now")
    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
            self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skip("not right now")
    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    @unittest.skip(" not needed. ")
    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertFalse(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
            self.assertNotEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    @unittest.skip("not needed")
    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    @unittest.skip("not right now")
    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    @unittest.skip(" not right now")
    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage.FileStorage.__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    @unittest.skip("not needed ")
    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
            self.assertEqual(temp, 'BaseModel' + '.' + _id)

    @unittest.skip("not needed ")
    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        # print(type(storage))
        self.assertEqual(type(storage), DBStorage)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip if not fs")
class TestFileStorageCount(unittest.TestCase):
    """Tests the count() method of the FileStorage class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = FileStorage()
        self.storage.reload()

        # Clear the storage
        for key in list(self.storage.all().keys()):
            del self.storage._FileStorage__objects[key]
        self.storage.save()

        self.objects_to_create = {
            State: [("California",), ("New York",), ("Texas",)],
            Place: [("Home",), ("Office",)]
        }
        self.created_objects = []

        for obj_class, obj_data in self.objects_to_create.items():
            for obj_args in obj_data:
                obj = obj_class(*obj_args)
                obj.save()
                self.created_objects.append(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip if not fs")
class TestFileStorageCountMore(unittest.TestCase):
    def setUp(self):
        self.state = State(name="California")
        self.state.save()

    def tearDown(self):
        storage.delete(self.state)
        storage.save()

    def test_count_all(self):
        count_all = storage.count()
        self.assertIsInstance(count_all, int)
        self.assertGreaterEqual(count_all, 1)

    def test_count_specific_class(self):
        count_state = storage.count(State)
        self.assertIsInstance(count_state, int)
        self.assertEqual(count_state, 1)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "skip if db")
class TestFileStorageGet(unittest.TestCase):
    """Tests get method of the FileStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = FileStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_get_existing_object(self):
        """Test get() with an object that exists"""
        obj = self.storage.get(State, self.new_state.id)
        self.assertEqual(obj.id, self.new_state.id)

    def test_get_nonexistent_object(self):
        """Test get() with an object that does not exist"""
        obj = self.storage.get(State, "nonexistent")
        self.assertIsNone(obj)