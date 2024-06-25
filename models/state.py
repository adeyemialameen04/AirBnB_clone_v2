#!/usr/bin/python3
"""Documenting the user model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class State(BaseModel, Base):
    """The state class"""
    __tablename__ = "states"
    name = Column("name", String(128), nullable=False)

    # name = ""
