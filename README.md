# yodl

Build Django models from YAML configuration files.

---

Take the following example:

`models.py`
```python
from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=200)
    published_on = models.DateTimeField('date published')

    def __str__(self):
      return self.text

class Choice(models.Model):
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
      return self.text
```

With `yodl`, you can define the model properties in a separate YAML file
and decorate the class with it.

`Question.yaml`
```yaml
text:
  type: CharField
  max_length: 200
  unique: True

published_on:
  type: DateTimeField
  args:
    - date published
```

`Choice.yaml`
```yaml
text:
  type: CharField
  max_length: 200

votes:
  type: IntegerField
  default: 0

question:
  type: ForeignKey
  args:
    - Question
  on_delete: $models.CASCADE
  ```

`models.py`
```python
from django.db import models

@yodl
class Question(models.Model):
    def __str__(self):
      return self.text

@yodl
class Choice(models.Model):
    def __str__(self):
      return self.text
```

Usage is as you would expect:

```shell
$ python manage.py shell
>>> from mysite.models import Question, Choice
>>> Question.text
<django.db.models.query_utils.DeferredAttribute object at 0x105a0bda0>
>>> Question.published_on
<django.db.models.query_utils.DeferredAttribute object at 0x105a0bd30>
>>> Choice.question
<django.db.models.fields.related_descriptors.ForwardManyToOneDescriptor object at 0x1059edc50>
>>> from django.utils import timezone
>>> question = Question.objects.create(text="""
... According to the Standard Model of elementary particles,
... which of the following is not a composite object?
... """.strip().replace('\n', ' '),
... published_on=timezone.now())
>>> _ = [Choice.objects.create(text=t, question=question) for t in [
...'Muon', 'Pi-meson', 'Neutron', 'Deuteron', 'Alpha particle'
...]
>>> _ = [print(choice) for choice in question.choice_set.all()]
Choice: Muon
Choice: Pi-meson
Choice: Neutron
Choice: Deuteron
Choice: Alpha particle
```
