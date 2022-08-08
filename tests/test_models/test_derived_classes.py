#!/usr/bin/python3
"""Testing all the classes that derive from BaseModel class"""

from os import remove
import unittest
from datetime import datetime

from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User
from models.__init__ import storage


class TestUser(unittest.TestCase):
    """Testing all the classes that derive from BaseModel class"""

    def tearDown(self):
        """destroy test object for all tests"""
        try:
            remove('file.json')
        except FileNotFoundError:
            pass

    def check_object(self, obj, key):
        """tests the objects

        Args:
            obj (object): the object to be checked
            key (string): the key to be checked
        """
        obj.save()
        objs = storage.all()

        self.assertTrue(key in objs)
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

        self.assertEqual(objs[key]['__class__'], f'{obj.__class__.__name__}')

    def test_User(self):
        """tests the  class"""
        Jack = User()
        Jack.first_name = "Jack"
        Jack.last_name = "Hemp"
        Jack.email = "jackhemp@gmail.com"
        Jack.password = "J@ckHemp"
        Jack.id = "JackHemp"

        self.check_object(Jack, "User.JackHemp")

    def test_Amenity(self):
        """tests the Amenity class"""
        Waikiki_Plaza = Amenity()
        Waikiki_Plaza.name = "The Plaza at Waikiki"
        Waikiki_Plaza.id = "Waikiki_Plaza"

        self.check_object(Waikiki_Plaza, "Amenity.Waikiki_Plaza")

    def test_City(self):
        """tests the City class"""
        Honolulu = City()
        Honolulu.state_id = "Hawaii"
        Honolulu.name = "Honolulu"
        Honolulu.id = "Honolulu"

        self.check_object(Honolulu, "City.Honolulu")

    def test_Place(self):
        """tests the Place class"""
        MarriottResort = Place()
        MarriottResort.id = "MarriottResort"
        MarriottResort.city_id = "Honolulu"
        MarriottResort.user_id = "JackHemp"
        MarriottResort.name = "Waikiki Beach Marriott Resort & Spa"
        MarriottResort.description = \
            "Ocean View, Guest Room, 2 Double, Paoakalani Tower, Balcony"
        MarriottResort.number_rooms = 1
        MarriottResort.number_bathrooms = 1
        MarriottResort.max_guest = 4
        MarriottResort.price_by_night = 6499
        MarriottResort.latitude = 21.273895
        MarriottResort.longitude = -157.822518

        self.check_object(MarriottResort, "Place.MarriottResort")

    def test_Review(self):
        """tests the Review class"""
        Marriott_Review = Review()
        Marriott_Review.place_id = "MarriottResort"
        Marriott_Review.user_id = "JackHemp"
        Marriott_Review.text = "Lorem ipsum dolor sit amet, consectetuer."
        Marriott_Review.id = "Marriott_Review"

        self.check_object(Marriott_Review, "Review.Marriott_Review")


    def test_State(self):
        """tests the State class"""
        Hawaii = State()
        Hawaii.name = "Hawaii"
        Hawaii.id = "Hawaii"

        self.check_object(Hawaii, "State.Hawaii")
