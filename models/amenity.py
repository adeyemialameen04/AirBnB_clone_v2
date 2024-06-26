#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from envs import HBNB_TYPE_STORAGE
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    The amenity class
    """
    __tablename__ = "amenities"
    if HBNB_TYPE_STORAGE != "db":
        name = ""
    else:
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       back_populates="amenities")
