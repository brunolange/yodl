import yaml
from yodl import yodl, yodlify

from django.test import TestCase
from django.db import models
from django.utils import timezone

from testapp.models import Question, Choice

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

# Create your tests here.
class TestYodl(TestCase):
    """Main tester class
    """

    def setUp(self):
        self.text = ' '.join([
            'According to the Standard Model of elementary particles',
            'which of the following is not a composite object?'
        ])
        question = Question.objects.create(
            text=self.text,
            published_on=timezone.now()
        )
        Choice.objects.bulk_create([
            Choice(text=t, question=question) for t in [
                'Muon', 'Pi-meson', 'Neutron', 'Deuteron', 'Alpha particle'
            ]
        ])

    def test_question_model(self):
        """test sample question model
        """
        cls = models.query_utils.DeferredAttribute
        self.assertTrue(isinstance(Question.text, cls))
        self.assertTrue(isinstance(Question.published_on, cls))

        question = Question.objects.first()
        self.assertEqual(question.text, self.text)

    def test_choice_model(self):
        """test sample choice model
        """
        cls = models.query_utils.DeferredAttribute
        self.assertTrue(isinstance(Choice.text, cls))
        self.assertEqual(set(c.text for c in Choice.objects.all()), {
            'Muon', 'Pi-meson', 'Neutron', 'Deuteron', 'Alpha particle'
        })


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
