#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
        "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            filtered_obj = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    filtered_obj[key] = value
            return filtered_obj

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """deletes obj from objects"""
        if obj is not None:
            key = key = obj.__class__.__name__ + "." + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """ updating file storage """
        self.reload()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def get(self, cls, id):
        """ retrives one object and return it"""
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for temp in all_cls.values():
            if temp.id == id:
                return temp
        
        return None

    def count(self, cls=None):
        """ count number of objects in storage """
        all_classes = classes.values()
        if not cls:
            count = 0
            for temp in all_classes:
                count += len(models.storage.all(temp).values())
        else:
            count = len(models.storage.all(cls).values())
        return 0
