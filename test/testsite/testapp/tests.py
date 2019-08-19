import yaml
from yodl import yodl, yodlify

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


class TestYodlify(TestCase):
    def test_yodlify(self):
        qyaml = yodlify(Question)
        qdict = yaml.load(qyaml, Loader=yaml.FullLoader)

        self.assertTrue('text' in qdict)
        text = qdict['text']
        self.assertEqual(text['type'], 'CharField')
        self.assertEqual(text['max_length'], 200)
        self.assertEqual(text['unique'], True)

        self.assertTrue('published_on' in qdict)
        published_on = qdict['published_on']
        self.assertEqual(published_on['type'], 'DateTimeField')
        self.assertEqual(published_on['args'], ['date published'])

        cyaml = yodlify(Choice)
        cdict = yaml.load(cyaml, Loader=yaml.FullLoader)

        self.assertTrue('text' in cdict)
        text = cdict['text']
        self.assertEqual(text['type'], 'CharField')
        self.assertEqual(text['max_length'], 200)
        self.assertEqual(text['unique'], False)

        self.assertTrue('votes' in cdict)
        votes = cdict['votes']
        self.assertEqual(votes['type'], 'IntegerField')
        self.assertEqual(votes['default'], 0)

        self.assertTrue('question' in cdict)
        question = cdict['question']
        self.assertEqual(question['type'], 'ForeignKey')
        self.assertEqual(question['args'], ['Question'])
        self.assertEqual(question['on_delete'], '$models.CASCADE')
