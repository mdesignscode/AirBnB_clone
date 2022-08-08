#!/usr/bin/python3
"""Testing the base_model module"""

import json
import unittest
from os import remove

from datetime import datetime
from models.base_model import BaseModel
from models.__init__ import storage, FileStorage


class TestBaseModel(unittest.TestCase):
    """Testing the BaseModel class"""

    def setUp(self):
        """test object for all tests"""
        self.my_model = BaseModel()
        self.my_model.name = "First_Model"
        self.my_model.my_number = 98

    def tearDown(self):
        """destroy test object for all tests"""
        try:
            remove('file.json')
        except FileNotFoundError:
            pass

    def test_initialization(self):
        """tests the initialization of class"""

        # check instance attribute types
        self.assertIsInstance(self.my_model.id, str)
        self.assertIsInstance(self.my_model.created_at, datetime)
        self.assertIsInstance(self.my_model.updated_at, datetime)

        new_model = BaseModel(**self.my_model.to_dict())
        self.assertIsInstance(new_model.id, str)
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)
        self.assertTrue(hasattr(new_model, "id"))
        self.assertTrue(hasattr(new_model, "updated_at"))
        self.assertTrue(hasattr(new_model, "created_at"))
        self.assertTrue(hasattr(new_model, "__class__"))
        self.assertTrue(hasattr(new_model, "name"))
        self.assertTrue(hasattr(new_model, "my_number"))

    def test_save_method(self):
        """tests the save method"""
        time = self.my_model.updated_at
        self.my_model.save()
        self.assertNotEqual(self.my_model.updated_at, time)

    def test_to_dict_method(self):
        """tests the to_dict method"""
        my_dict = self.my_model.to_dict()

        # check for attributes
        self.assertIn("__class__", my_dict)
        self.assertIn("id", my_dict)
        self.assertIn("updated_at", my_dict)
        self.assertIn("created_at", my_dict)
        self.assertIn("name", my_dict)
        self.assertIn("my_number", my_dict)

        # check attribute types
        self.assertIsInstance(my_dict['id'], str)
        self.assertIsInstance(my_dict['created_at'], str)
        self.assertIsInstance(my_dict['updated_at'], str)
