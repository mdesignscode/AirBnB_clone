#!/usr/bin/python3
"""
    serializes instances to a JSON file and
    deserializes JSON file to instances
"""
import json


class FileStorage:
    """serializes/deserializes an object

        Attributes:
            __file_path (string): path to the JSON file
            __objects (dict): will store all objects by <class name>.id
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as file:
                self.__objects = json.load(file)

        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
