from django.db import models

from yodl import yodl


@yodl
class Question(models.Model):
    pass


@yodl
class Choice(models.Model):
    pass
