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

`models.py`
```python
from django.db import models

@yodl
class Question(models.Model):
    pass
```

```shell
$ python manage.py shell
>>> from mysite.models import Question
>>> Question.text
<django.db.models.query_utils.DeferredAttribute object at 0x105a0bda0>
>>> Question.published_on
<django.db.models.query_utils.DeferredAttribute object at 0x105a0bd30>
```
