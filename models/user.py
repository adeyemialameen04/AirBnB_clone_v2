#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel


class User(BaseModel):
    """The user class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
