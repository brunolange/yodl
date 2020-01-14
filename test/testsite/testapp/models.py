import sys

from django.db import models

sys.path.append('../..')
from yodl import yodl


@yodl
class Question(models.Model):
    pass


@yodl
class Choice(models.Model):
    pass
