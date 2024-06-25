#!/usr/bin/python3
"""Documenting the user model"""
from envs import HBNB_TYPE_STORAGE
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """The user class"""
    __tablename__ = "users"
    if HBNB_TYPE_STORAGE == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
