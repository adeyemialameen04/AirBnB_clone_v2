#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from envs import HBNB_TYPE_STORAGE
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """The review class"""
    __tablename__ = "reviews"
    if HBNB_TYPE_STORAGE != "db":
        place_id = ""
        user_id = ""
        text = ""

    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
