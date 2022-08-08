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
        """sets in __objects the obj with key <obj class name>.id

            Args:
                obj (object): the object to be set
        """
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """serializes __objects to the JSON file"""
        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file)
            file.write("\n")

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r") as file:
                self.__objects = json.load(file)

        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def destroy(self, obj):
        """removes an object from __objects

        Args:
            obj (string): the name of the object to be removed
        """
        try:
            self.__objects.__delitem__(obj)
            self.save()
            self.reload()
        except KeyError:
            return

    def update(self, obj_class, obj_id, attr_name, attr_val):
        """adds/updates an instance attribute

        Args:
            obj_class (str): the class of the object
            obj_id (str): the id of the object to be updated
            attr_name (str): the name of the attribute to add/update
            attr_val (any): the value to be added/updated
                            this value will be casted to str
        """
        obj_name = f"{obj_class}.{obj_id}"
        self.__objects[obj_name][attr_name] = attr_val
        self.save()
        self.reload()
