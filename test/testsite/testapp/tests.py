# import sys
# import os
# sys.path.append(os.path.join('..', '..'))
from yodl import yodl

from django.test import TestCase
from django.db import models

from testapp.models import Question, Choice

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

# Create your tests here.
class TestYodl(TestCase):
    """Main tester class
    """
    def test_question_model(self):
        """test sample question model
        """
        cls = models.query_utils.DeferredAttribute
        self.assertTrue(isinstance(Question.text, cls))
        self.assertTrue(isinstance(Question.published_on, cls))

    def test_choice_model(self):
        """test sample choice model
        """
        cls = models.query_utils.DeferredAttribute
        self.assertTrue(isinstance(Choice.text, cls))
