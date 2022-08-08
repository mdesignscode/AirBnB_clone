#!/usr/bin/python3
"""Testing the console module"""

from datetime import datetime
from os import remove
import unittest
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

from models import storage
from user import User

all = storage.all


class TestHBNBCommand(unittest.TestCase):
    """Testing the HBNBCommand class"""

    def check_message(self, command, expected="** class name missing **"):
        """tests that an expected error message is printed

        Args:
            command (string): the command to be executed
            expected (string): the error message expected"""
        try:
            remove('file.json')
        except FileNotFoundError:
            pass

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
            self.assertEqual(f.getvalue().rstrip(), expected)

    def setUp(self):
        """create test objects for all tests"""
        args = {'id': 'MildredHarmon',
                'created_at': '2048-08-07T14:06:39.126129',
                '__class__': 'User',
                'first_name': "Mildred",
                'last_name': "Harmon",
                'email': "MildredHarmon@email.com",
                'password': '44ffe4d770b09e7d',
                'updated_at': '2048-08-07T14:06:39.126129'}
        self.user = User(**args)
        self.user.save()

        self.cli = HBNBCommand()

    def tearDown(self):
        """deletes the objects file"""
        try:
            remove('file.json')
        except FileNotFoundError:
            pass

    # create
    def test_create_no_class(self):
        """tests create with no class name"""
        self.check_message('create')

    def test_create_invalid_class(self):
        """tests create with invalid class name"""
        self.check_message('create InvalidClass',
                           "** class doesn't exist **")

    def test_create_valid_class(self):
        """tests create with valid class"""
        with patch('uuid.uuid4', return_value='Cayenne'):
            self.check_message('create City', 'Cayenne')

    # show
    def test_show_no_class(self):
        """tests show with no class name"""
        self.check_message('show')

    def test_show_invalid_class(self):
        """tests show with invalid class name"""
        self.check_message('show InvalidClass',
                           "** class doesn't exist **")

    def test_show_no_id(self):
        """tests show with no id"""
        self.check_message('show User',
                           '** instance id missing **')

    def test_show_invalid_id(self):
        """tests show with invalid id"""
        self.check_message('show User invalid-id', '** no instance found **')

    # destroy
    def test_destroy_no_class(self):
        """tests destroy with no class name"""
        self.check_message('destroy')

    def test_destroy_invalid_class(self):
        """tests destroy with invalid class name"""
        self.check_message('destroy InvalidClass',
                           "** class doesn't exist **")

    def test_destroy_no_id(self):
        """tests destroy with no id"""
        self.check_message('destroy User', '** instance id missing **')

    def test_destroy_invalid_id(self):
        """tests destroy with invalid id"""
        self.check_message('destroy User invalid-id',
                           '** no instance found **')

    def test_destroy_valid_id(self):
        """tests destroy with valid id"""
        self.cli.do_destroy('City Cayenne')
        self.check_message('show City Cayenne',
                           '** no instance found **')

    # show
    def test_show_no_class(self):
        """tests show no class name"""
        self.check_message('show')

    def test_show_invalid_class(self):
        """tests show invalid class name"""
        self.check_message('show Invalid', "** class doesn't exist **")

    def test_show_no_id(self):
        """tests show no id"""
        self.check_message('show User', '** instance id missing **')

    def test_show_invalid_id(self):
        """tests invalid id"""
        self.check_message('show User invalid-id', '** no instance found **')

    # update
    def test_update_no_class(self):
        """tests update no class name"""
        self.check_message('update')

    def test_update_invalid_class(self):
        """tests update invalid class name"""
        self.check_message('update InvalidClass',
                           "** class doesn't exist **")

    def test_update_no_id(self):
        """tests update no id"""
        self.check_message('update User', '** instance id missing **')

    def test_update_invalid_id(self):
        """tests update invalid id"""
        self.check_message('update User invalid-id',
                           '** no instance found **')

    def test_update_no_attribute_name(self):
        """tests update no attribute name"""
        self.check_message('update User MildredHarmon',
                           "** attribute name missing **")

    def test_update_no_attribute_value(self):
        """tests update no attribute value"""
        self.check_message('update User MildredHarmon name',
                           "** value missing **")

    def test_update_valid_id(self):
        """tests update with valid args"""
        self.cli.do_update('User MildredHarmon age 36')
        self.assertEqual(all()['User.MildredHarmon']['age'], 36)
        self.assertIs(type(all()['User.MildredHarmon']['age']), int)

        self.cli.do_update('User MildredHarmon name Mildred Harmon')
        self.assertEqual(all()['User.MildredHarmon']['name'], 'Mildred')

        self.cli.do_update('User MildredHarmon name "Mildred Harmon"')
        self.assertEqual(all()['User.MildredHarmon']['name'], 'Mildred Harmon')

    def test_update_valid_id_extra_args(self):
        """tests update only first attribute value and one update"""
        self.cli.do_update('User MildredHarmon age [36] foo bar')
        self.assertEqual(all()['User.MildredHarmon']['age'], [36])
        self.assertIs(type(all()['User.MildredHarmon']['age']), list)

        self.cli.do_update('User MildredHarmon name "Mildred Harmon" foo bar')
        self.assertEqual(all()['User.MildredHarmon']['name'], 'Mildred Harmon')

    def test_count_objects(self):
        """tests the <class name>.count() command"""
        self.check_message('BaseModel.count()', '0')

        states = ["Guernsey", "Mexico", "Peru", "Greece", "Indonesia"]
        for state in states:
            with patch('uuid.uuid4', return_value=state):
                self.check_message('create State', state)

        self.check_message('BaseModel.count()', '0')
        self.check_message('City.count()', '0')
        self.check_message('State.count()', '5')

    def test_dot_commands(self):
        """tests the <class name>.<action>() commands"""
        key = 'Amenity.MontBourda'
        with patch('uuid.uuid4', return_value='MontBourda'):
            self.check_message('Amenity.create()', 'MontBourda')

        self.check_message('Amenity.show()', '** instance id missing **')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.show(MontBourda)')
            self.assertNotEqual(f.getvalue().rstrip(),
                                '** no instance found **')
            HBNBCommand().onecmd('Amenity.show("MontBourda")')
            self.assertNotEqual(f.getvalue().rstrip(),
                                '** no instance found **')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.destroy(MontBourda)')
            self.assertNotEqual(f.getvalue().rstrip(),
                                '** no instance found **')
            self.check_message('Amenity.show("MontBourda")',
                               '** no instance found **')

        with patch('uuid.uuid4', return_value='MontBourda'):
            self.check_message('Amenity.create()', 'MontBourda')

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity.destroy("MontBourda")')
            self.check_message('Amenity.show(MontBourda)',
                               '** no instance found **')

        with patch('uuid.uuid4', return_value='MontBourda'):
            self.check_message('Amenity.create()', 'MontBourda')

        self.check_message('InvalidClass.update()',
                           "** class doesn't exist **")
        self.check_message('Amenity.update()', '** instance id missing **')
        self.check_message('Amenity.update("MontBourda")',
                           "** attribute name missing **")
        self.check_message('Amenity.update("MontBourda" "name")',
                           "** value missing **")
        self.check_message('Amenity.update("invalid" "name" "Mont Bourda")',
                           '** no instance found **')

        self.check_message(
            'Amenity.update("MontBourda" "name" "Mont Bourda"', '')
        self.assertEqual(all()[key]['name'], "Mont Bourda")

        self.check_message(
            'Amenity.update("MontBourda" "citizens" "57614"', '')
        self.assertIs(type(all()[key]['citizens']), int)

        self.check_message(
            'Amenity.update("MontBourda" "name" "Mont Bourda" "foo bar"', '')
        self.assertEqual(all()[key]['name'], "Mont Bourda")

    def test_update_using_dictionary(self):
        """tests the <class name>.update(<id>, <dictionary>) action"""
        with patch('uuid.uuid4', return_value='MontBourda'):
            self.check_message('Amenity.create()', 'MontBourda')
        key = 'Amenity.MontBourda'
        self.check_message(
            'Amenity.update("MontBourda", {"area": 23.6, "has_sea": True})', "")
        self.assertEqual(all()[key]['area'], 23.6)
        self.assertIs(type(all()[key]['area']), float)
        self.assertEqual(all()[key]['has_sea'], True)
        self.assertIs(type(all()[key]['has_sea']), bool)

        mes = 'Amenity.update("MontBourda", ' \
            + '{"state_id": "French Guiana", "insee": 9730297300})'
        self.check_message(mes, "")
        self.assertEqual(all()[key]['state_id'], "French Guiana")
        self.assertIs(type(all()[key]['state_id']), str)
        self.assertEqual(all()[key]['insee'], 9730297300)
        self.assertIs(type(all()[key]['insee']), int)
