#!/usr/bin/python3
"""Testing the file_storage module"""


import json
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Testing the FileStorage class"""

    def setUp(self):
        self.storage = FileStorage()
        self.model = BaseModel()
        self.model.name = "First_Model"
        self.model.my_number = 98
        self.dict = self.model.to_dict()
        self.objects = {f'BaseModel.{self.model.id}': self.dict}

    def test_new_method(self):
        """tests the new_method"""
        self.storage.new(self.model)
        objects = self.storage.all()
        self.assertTrue(self.objects.items() <= objects.items())

    def test_save_method(self):
        """tests the save method"""
        self.storage.save()
        with open('file.json', "r") as file:
            data = json.load(file)

        self.storage.reload()
        objects = self.storage.all()
        self.assertTrue(objects.items() == data.items())

    def test_destroy_method(self):
        """tests the destroy method"""
        my_model = BaseModel()
        my_model.name = "Andromeda"
        my_model.type = "Galaxy"
        my_model.distance_from_earth = "4.2 light years"

        my_model.save()
        self.storage.reload()
        self.storage.destroy(f'BaseModel.{my_model.id}')
        all = self.storage.all()

        self.assertFalse(all.__contains__(f'BaseModel.{my_model.id}'))
