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
        """Db storage"""
        conn_str = f"mysql+mysqldb://{HBNB_MYSQL_USER}:{
            HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}"

        self.__engine = create_engine(conn_str, pool_pre_ping=True)

        if HBNB_ENV == "test":
            metadata = MetaData(bind=DBStorage.__engine)
            all_table = metadata.sorted_tables

            for table in all_table:
                table.drop(self.__engine)

    def all(self, cls=None):
        """Gets all instances"""
        if cls is None:
            object = self.__session.query(
                City).all() + self.__session.query(State).all()
            return {f"{obj.__class__.__name__}": obj for obj in object}
        else:
            className = classes[cls]
            object = self.__session.query(className).all()
            return {f"{obj.__class__.__name__}": obj for obj in object}

    def new(self, obj):
        """New instance"""
        self.__session.add(obj)

    def save(self):
        """Saves instance"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload db"""
        Base.metadata.create_all(bind=self.__engine)

        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.remove()
