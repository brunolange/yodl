"""Test suite for yodl decorator.
"""

import unittest
from django.db import models
from yodl import yodl

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

class TestYodl(unittest.TestCase):
    """Main tester class
    """
    def test_question_model(self):
        """test sample question model
        """
        @yodl('test/Question.yaml')
        class Question:
            pass
        self.assertTrue(isinstance(Question.text, models.CharField))
        self.assertTrue(isinstance(Question.published_on, models.DateTimeField))
