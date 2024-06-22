#!/usr/bin/python3
"""Filestorage model"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity


class FileStorage:
    """
    Filestorage class.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, obj=None):
        """
        Returns all the objs in the storage.
        :return: all the objs in the storage.
        """
        if obj is not None:
            filtered_dict = {}
            for key, value in FileStorage.__objects.items():
                if isinstance(value, obj):
                    filtered_dict[key] = value
            return filtered_dict
        return FileStorage.__objects

    def delete(self, obj=None):
        """Delete object"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def new(self, obj):
        """
        Creates a new obj in the storage.
        :param obj: The obj to be created.
        :return: Nothing
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Saves an obj to the storage.
        :return: Nothing.
        """
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Reloads the storage.
        :return: Nothing.
        """
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    dict_obj = json.loads(file.read())
                except json.JSONDecodeError:
                    return
                for key, value in dict_obj.items():
                    class_name = key.split(".")[0]
                    obj = globals()[class_name](**dict_obj[key])
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass
