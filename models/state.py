#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from envs import HBNB_TYPE_STORAGE
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State docs"""
    __tablename__ = 'states'
    if HBNB_TYPE_STORAGE == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """Joined cities"""
            from models import storage
            joined_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    joined_cities.append(city)
            return joined_cities
