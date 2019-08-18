import sys
sys.path.append('/Users/blangera/dev/yodl')
from yodl import yodl

from django.test import TestCase
from django.db import models

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
        @yodl('Question.yaml')
        class ModelQuestion(models.Model):
            pass

        self.assertTrue(isinstance(ModelQuestion.text, models.query_utils.DeferredAttribute))
        self.assertTrue(isinstance(ModelQuestion.published_on, models.query_utils.DeferredAttribute))
