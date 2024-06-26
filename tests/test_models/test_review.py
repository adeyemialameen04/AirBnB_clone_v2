#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from envs import HBNB_TYPE_STORAGE


class test_review(test_basemodel):
    """ review test class"""

    def __init__(self, *args, **kwargs):
        """ review class init"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ testing review place_id attr"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         HBNB_TYPE_STORAGE != 'db' else
                         type(None))

    def test_user_id(self):
        """ testing review user_id attr"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         HBNB_TYPE_STORAGE != 'db' else
                         type(None))

    def test_text(self):
        """ testing review text attr"""
        new = self.value()
        self.assertEqual(type(new.text), str if
                         HBNB_TYPE_STORAGE != 'db' else
                         type(None))
