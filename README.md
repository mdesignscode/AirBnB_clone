Description of Project ::
The Command Interpreter is used to manage the whole application's functionality from the command line, such as:

    Create a new object (ex: a new User or a new Place)
    Retrieve an object from a file, a database etc…
    Do operations on objects (count, compute stats, etc…)
    Update attributes of an object
    Destroy an object

Only “simple” arguments can be updated: string, integer and float.

A string argument with a space must be between double quote


Command interpreter:

to start interpreter :
```
$ ./console.py
```

******************************

examples of using interpreter:

```
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

Miscellaneous help topics:
==========================
extra_commands

(hbnb) help create
Creates a new instance of BaseModel and prints the id
Usage: create <class name>

valid classes ::
BaseModel
User
Amenity
City
Place
State
Review

(hbnb) create User
ba7a07ac-9d84-4507-a089-58c90f7493c2
(hbnb) User.destroy(ba7a07ac-9d84-4507-a089-58c90f7493c2)
(hbnb) create Pie
** class doesn't exist **
(hbnb) show User ba7a07ac-9d84-4507-a089-58c90f7493c2
** no instance found **
```

**********************************************************

using interpreter in non-interactive mode

```
$ echo "create Pie" | ./console.py
(hbnb) ** class doesn't exist **
(hbnb)
$ echo "all" | ./console.py
(hbnb) []
(hbnb)
```

**********************************************************

**commands ::**
| create  | Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id. Ex: $ create BaseModel  |
|---|---|
|  show | Prints the string representation of an instance based on the class name and id. Ex: $ show BaseModel 1234-1234-1234  |
|  destroy | Deletes an instance based on the class name and id.  Ex: $ destroy BaseModel 1234-1234-1234.   |
|  all | Prints all string representation of all instances based or not on the class name. Ex: $ all BaseModel or $ all  |
|  update |  Updates an instance based on the class name and id by adding or updating attribute. Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".  |
