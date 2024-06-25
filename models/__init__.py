#!/usr/bin/python3
"""Decide weather to use the db or local"""
from envs import HBNB_TYPE_STORAGE
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

if HBNB_TYPE_STORAGE == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
