#!/usr/bin/python3
"""Documenting the console module"""
import ast
import cmd
import shlex
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """Documentation for the console"""

    methods = ["all()", "count()"]

    prompt = "(hbnb) "

    def do_clear(self, arg):
        print("\033[2J\033[H", end="", flush=True)

    def convert_value(self, key, value):
        if key in ['number_rooms', 'number_bathrooms', 'max_guest', 'price_by_night']:
            return int(value)
        elif '.' in value:
            return float(value)
        else:
            print("\n\n", value, "\n\n")
            return value.replace("_", " ")

    def parse_arg(self, arg):
        args = shlex.split(arg)
        argc = len(args)
        if argc == 0:
            print("** class name missing **")
            return None, None, None

        name = args[0]
        cls = globals().get(name)
        if cls is None:
            print("** class doesn't exist **")
            return None, None, None

        if argc < 2:
            return cls, None, None

        inst_id = args[1]
        key = f"{name}.{inst_id}"
        if key not in storage.all():
            print("** no instance found **")
            return None, None, None

        return cls, inst_id, args[2:]

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class."""
        args = shlex.split(arg)
        argc = len(args)
        if argc == 0:
            print("** class name missing **")
            return

        name = args[0]

        cls = globals().get(name)
        if cls is None:
            print("** class doesn't exist **")
            return
        obj = cls()
        if argc == 1:
            obj.save()
            print(obj.id)
            return
        if argc > 1:
            key = f"{name}.{obj.id}"
            params_dict = {}
            for item in args[1:]:
                key, value = item.split("=")
                params_dict[key] = self.convert_value(key, value)
            for key, value in params_dict.items():
                setattr(obj, key, value)
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Shows an inst of a class."""
        cls, inst_id, _ = self.parse_arg(arg)
        if inst_id is None and cls is not None:
            print("** instance id missing **")
            return
        if cls and inst_id:
            key = f"{cls.__name__}.{inst_id}"
            print(storage.all()[key])

    def do_destroy(self, arg):
        """Destroys an inst of a class."""
        cls, inst_id, _ = self.parse_arg(arg)
        if inst_id is None and cls is not None:
            print("** instance id missing **")
            return
        if cls and inst_id:
            key = f"{cls.__name__}.{inst_id}"
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """Gets all."""
        args = shlex.split(arg)
        argc = len(args)
        objs = []
        if argc == 0:
            for obj in storage.all().values():
                objs.append(str(obj))
            print(objs)
            return

        name = args[0]
        cls = globals().get(name)
        if cls is None:
            print("** class doesn't exist **")
            return

        cls.all(self, name)

    def do_update(self, arg):
        """Updates"""
        args = shlex.split(arg)
        argc = len(args)
        if argc == 0:
            print("** class name missing **")
            return
        name = args[0]
        cls = globals().get(name)
        if cls is None:
            print("** class doesn't exist **")
            return

        if argc < 2:
            print("** instance id missing **")
            return

        ist_id = args[1]
        key = f"{name}.{ist_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if argc < 3:
            print("** attribute name missing **")
            return

        attr_name = args[2]

        if argc < 4:
            print("** value missing **")
            return

        attr_val = args[3]

        obj = storage.all()[key]
        setattr(obj, attr_name, attr_val)
        obj.save()

    def default(self, arg):
        match = re.match(r"(\w+)\.(\w+)\((.*)\)", arg)
        if match:
            match_tup = match.groups()
            name, method, method_args = match_tup
            cls = globals().get(name)
            if cls is None:
                print("** class doesn't exist **")
                return

            if method == "all":
                cls.all(self, name)
            elif method == "count":
                cls.count(self, name)
            elif method == "show":
                inst_id = method_args.strip("\"'")
                if inst_id == "":
                    print("** instance id missing **")
                    return
                key = f"{cls.__name__}.{inst_id}"
                if key not in storage.all():
                    print("** no instance found **")
                    return
                print(storage.all()[key])
            elif method == "destroy":
                inst_id = method_args.strip("\"'")
                if inst_id == "":
                    print("** instance id missing **")
                    return
                key = f"{cls.__name__}.{inst_id}"
                if key not in storage.all():
                    print("** no instance found **")
                    return
                del storage.all()[key]
                storage.save()
            elif method == "update":
                last = match_tup[2]
                shlex_args = shlex.split(last)
                print(shlex_args)
                inst_id = shlex_args[0][:-1]
                if len(shlex_args) == 3:
                    attr_name = shlex_args[1][:-1]
                    attr_val = shlex_args[2]
                    if id == "":
                        print("** instance id missing **")
                        return

                    key = f"{name}.{inst_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                        return

                    if attr_name == "":
                        print("** attribute name missing **")
                        return

                    if attr_val == "":
                        print("** value missing **")
                        return

                    obj = storage.all()[key]
                    setattr(obj, attr_name, attr_val)
                    obj.save()
                else:
                    pattern = r'"([^"]+)",\s*({.*})'
                    match = re.search(pattern, last)
                    if match:
                        inst_id, dict_str = match.groups()
                        obj_dict = ast.literal_eval(dict_str)
                        key = f"{name}.{inst_id}"
                        if key not in storage.all():
                            print("** no instance found **")
                            return

                        print(obj_dict)
                        obj = storage.all()[key]
                        for attr_name, attr_value in obj_dict.items():
                            setattr(obj, attr_name, attr_value)
                        obj.save()
            else:
                print("*** Unknown syntax:")
                return

        else:
            print(f"*** Unknown syntax: {arg}")
            return

    def emptyline(self):
        """Does nothing."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
