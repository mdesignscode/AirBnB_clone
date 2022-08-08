#!/usr/bin/python3
"""contains the entry point of the command interpreter"""

import cmd

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User


d_all = storage.all


class HBNBCommand(cmd.Cmd):
    """a custom command line interpreter to do
    operations on objects"""

    valid_classes = ["BaseModel", "User", "Amenity",
                     "City", "Place", "State", "Review"]
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """exits the program"""
        quit()

    def do_EOF(self, arg):
        """exits the program"""
        print()
        quit()

    def emptyline(self):
        pass

    def do_create(self, arg):
        """Creates a new instance of <class name>, saves it
        (to the JSON file) and prints the id"""
        if not len(arg):
            print("** class name missing **")
            return
        if arg not in self.valid_classes:
            print("** class doesn't exist **")
            return
        new_obj = eval(arg)()
        new_obj.save()
        storage.reload()
        print(new_obj.id)

    def help_create(self):
        """Creates a new instance of <class name>"""
        print("Creates a new instance of BaseModel and prints the id")
        print("Usage: create <class name>\n")
        print("valid classes ::")
        [print(c) for c in self.valid_classes]
        print()

    def do_show(self, args):
        """Prints the string representation of an
        instance based on the class name and id"""
        if not len(args):
            print("** class name missing **")
            return
        class_name = args.split()[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        try:
            id = args.split()[1]
        except IndexError:
            print("** instance id missing **")
            return

        objs = d_all()
        obj = f"{class_name}.{id}"
        if obj not in objs:
            print("** no instance found **")
            return

        new_obj = eval(class_name)(**objs[obj])
        print(new_obj)

    def help_show(self):
        """Prints the string representation of an
        instance based on the class name and id"""
        print('Prints the string representation of an instance', end=' ')
        print('based on the class name and id')
        print("Usage: show <class name> <id name>\n")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        if not len(args):
            print("** class name missing **")
            return
        class_name = args.split()[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        try:
            id = args.split()[1]
        except IndexError:
            print("** instance id missing **")
            return

        objs = d_all()
        obj = f"{class_name}.{id}"
        if obj not in objs:
            print("** no instance found **")
            return

        storage.destroy(obj)

    def help_destroy(self):
        """Deletes an instance based on the class name and id"""
        print('Deletes an instance based on the class name and id')
        print('Usage: destroy <class name> <id>\n')

    def do_all(self, args):
        """Prints all string representation of all instances
        based or not on the class name"""
        objs = d_all()
        models = []
        dictionaries = [values for values in objs.values()]
        for dictionary in dictionaries:
            if not len(args):
                class_name = dictionary['__class__']
                new_model = eval(class_name)(**dictionary)
                models.append(new_model.__str__())

            else:
                if args not in self.valid_classes:
                    print("** class doesn't exist **")
                    return
                if dictionary['__class__'] == args:
                    new_model = eval(args)(**dictionary)
                    models.append(new_model.__str__())
        print(models)

    def help_all(self):
        """Prints all string representation of all instances
        based or not on the class name"""
        print('Prints a list of string representations of all instances')
        print('Usage:\n(hbnb) all\nor\n(hbnb) all <class name>\n')

    def do_update(self, args):
        """updates/adds instance attributes"""
        lines = args.split(maxsplit=3)
        try:
            class_name = args.split()[0]
            if len(args) and class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return
        except IndexError:
            print("** class name missing **")
            return

        try:
            id = args.split()[1]
            if f"{class_name}.{id}" not in d_all() and len(args) > 1:
                print("** no instance found **")
                return
        except IndexError:
            print("** instance id missing **")
            return

        if len(lines) == 2:
            print("** attribute name missing **")
            return
        if len(lines) == 3:
            print("** value missing **")
            return

        if '"' in lines[3]:
            if len(lines[3].split('" ')) > 1:
                value = lines[3].split('" ')[0].lstrip('"')
            if len(lines[3].split('" ')) == 1:
                value = lines[3]

        else:
            value = lines[3].split()[0]

        try:
            storage.update(lines[0], lines[1], lines[2], eval(value))
        except NameError:
            storage.update(lines[0], lines[1], lines[2], value.strip('"'))
        except SyntaxError:
            storage.update(lines[0], lines[1], lines[2], value)

    def help_update(self):
        """updates/adds instance attributes"""
        print('updates or adds instance attributes')
        print("Only one attribute can be updated at the time\n")
        print(
            'Usage <class name> <id> <attribute name> <attribute value>')
        print(
            'A string argument with a space must be between double quote')
        print('for example, update User 15322ea name "Kate Welch"\n')

    def execute_class_name(self, class_name, action):
        """executes <class name>.command()

        Args:
            class_name (string): name of the class
            action (string): the action to be performed"""
        # <class name>.create()
        if action == 'create()':
            self.do_create(class_name)

        # <class name>.all()
        if action == "d_all()":
            self.do_all(class_name)

        # <class name>.count()
        if action == 'count()':
            objs = d_all()
            c = 0

            for value in objs.values():
                if value['__class__'] == class_name:
                    c = c + 1
            print(c)

        # <class name>.show("id")
        if action[:5] == "show(":
            if '"' in action:
                self.do_show(class_name + " " + action[6:-2])
            else:
                self.do_show(class_name + " " + action[5:-1])

        # <class name>.destroy("id")
        if action[:8] == "destroy(":
            if '"' in action:
                self.do_destroy(class_name + " " + action[9:-2])
            else:
                self.do_destroy(class_name + " " + action[8:-1])

        # <class name>.update("id", "attribute name", "attribute value")
        if action == 'update()':
            print('** instance id missing **')
            return
        nots = ['{' not in action, '}' not in action]
        if action[:7] == "update(" and all(nots):
            lines = action.split('"')
            if len(lines) == 3:
                print("** attribute name missing **")
                return
            if len(lines) == 5:
                print('** value missing **')
                return
            if action.count('"') < 6:
                print("Usage:")
                print('<class name>.update("<id>" "name" "value")\n')
                return
            value = '"' + lines[5] + '"'
            if len(eval(value).split()) == 1:
                value = eval(value)
            com = " ".join([class_name, lines[1], lines[3], value])
            self.do_update(com)

        # <class name>.update("id", {dict representation})
        if action[:7] == "update(" and not all(nots):
            lines = action.split(', ', 1)
            lines[1] = lines[1].replace("'", '"')
            id = lines[0][8:-1]
            my_dict = eval(lines[1].rstrip(")"))
            for key, value in my_dict.items():
                if type(value) is str:
                    com = f'{class_name} {id} {key} "{value}"'
                else:
                    com = f'{class_name} {id} {key} {value}'
                self.do_update(com)

    def default(self, line):
        """custom <class name>.<action>() commands"""
        lines = line.split(".", 1)
        if lines[0] in self.valid_classes and len(lines) > 1:
            self.execute_class_name(lines[0], lines[1])
        elif lines[0] not in self.valid_classes and len(lines) > 1:
            print("** class doesn't exist **")
            return
        else:
            super().default(line)

    def help_extra_commands(self):
        print("Usage: <class name>.<action>()")
        print('actions:')
        print('<class name>.all()')
        print(
            '<class name>.count() # counts the number of instances of a class')
        print('<class name>.show("<id>")')
        print('<class name>.destroy("<id>")')
        print('<class name>.create()')
        print('<class name>.update("<id"', end=' ')
        print('"<attribute name>" "<attribute value>")')
        print('for update using a dictionary:')
        print('<class name>.update("<id>" <dictionary representation>)\n')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
