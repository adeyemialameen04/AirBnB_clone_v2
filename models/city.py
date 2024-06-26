#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from envs import HBNB_TYPE_STORAGE


class City(BaseModel, Base):
    """The city class"""
    __tablename__ = "cities"
    if HBNB_TYPE_STORAGE != "db":
        name = ""
        state_id = ""
    else:
        name = Column("name", String(120), nullable=False)
        state_id = Column("state_id", String(
            60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities',
                              cascade='all, delete, delete-orphan')
