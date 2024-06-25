#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"
    name = Column("name", String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Intilizes states"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
        # id = Column(String(60), primary_key=True, nullable=False)
    else:
        @property
        def cities(self):
            import models
            from models.city import City
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
            # if value.to_dict()["state_id"] == self.id:
