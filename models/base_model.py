#!/usr/bin/python3
"""Base model"""
from datetime import datetime
from uuid import uuid4
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel:
    """BaseModel for Airbnb"""
    id = Column("id", String(60), primary_key=True, nullable=False)
    created_at = Column("created_at", DateTime,
                        nullable=False, default=datetime.utcnow())
    updated_at = Column("updated_at", DateTime,
                        nullable=False, default=datetime.utcnow(),
                        onupdate=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance.
        """
        if kwargs:
            dates_var = ["created_at", "updated_at"]
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in dates_var:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
        A string representation of the instance of BaseModel.
        :return: str
        """
        result_str = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return result_str

    def save(self):
        """
        Updates the updated_at.
        :return: Nothing.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        A dict representation of the class with more keys added.
        :return: The dict.
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        dates_var = ["created_at", "updated_at"]
        for key, value in obj_dict.items():
            if key in dates_var:
                obj_dict[key] = value.isoformat()

        if '_sa_instance_state' in obj_dict.keys():
            del obj_dict['_sa_instance_state']

        return obj_dict

    # def all(self, name):
    #     """
    #     Handles the class all for a particular name.
    #     :param name: The name of the class.
    #     :return: Nothing.
    #     """
    #     objs = []
    #
    #     for key, value in models.storage.all().items():
    #         if key.startswith(name):
    #             objs.append(str(value))
    #     print(objs)

    def count(self, name):
        """
        Counts the instances of the class.
        """
        count = 0
        for key in models.storage.all():
            if key.startswith(f"{name}"):
                count += 1

        print(count)

    def delete(self):
        """Commits suicide"""
        models.storage.delete(self)
