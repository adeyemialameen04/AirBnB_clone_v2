#!/usr/bin/python3
"""Module for the db storage """
import os
from sqlalchemy import MetaData, create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from envs import (
    HBNB_TYPE_STORAGE,
    HBNB_MYSQL_USER,
    HBNB_MYSQL_PWD,
    HBNB_MYSQL_HOST,
    HBNB_MYSQL_DB,
    HBNB_ENV
)


classes = {
    "User": User,
    "Place": Place,
    "City": City,
    "Amenity": Amenity,
    "Review": Review,
    "State": State
}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB
            ), pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Gets all instances"""
        obj_dict = {}
        if cls is None:
            for item in classes.values():
                for obj in self.__session.query(item).all():
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + '.' + obj.id
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """New instance"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """Saves instance"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Close session"""
        self.__session.remove()
