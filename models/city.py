#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """The city class"""
    __tablename__ = "cities"
    name = Column("name", String(120), nullable=False)
    state_id = Column("state_id", String(
        60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="city",
                          cascade="all, delete")
    # name = ""
    # state_id = ""
