#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """The user class"""
    __tablename__ = "users"
    email = Column("email", String(128), nullable=False)
    password = Column("password", String(128), nullable=False)
    first_name = Column("first_name", String(128), nullable=False)
    last_name = Column("last_name", String(128), nullable=False)
    # email = ""
    # password = ""
    # first_name = ""
    # last_name = ""
