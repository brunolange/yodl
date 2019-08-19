"""utility module for the yodl package
"""

from functools import reduce, partial
import yaml

from django.db import models

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

def _extend(*dicts):
    def _fold(acc, curr):
        acc.update(curr)
        return acc
    return reduce(_fold, dicts, {})

def _startswith(obj, char):
    return isinstance(obj, str) and obj and obj[0] == char

def _navigate(acc, curr):
    return acc[curr] if isinstance(acc, dict) else getattr(acc, curr)

def _parse_reduce(value):
    return reduce(_navigate, value.split('.'), {'models': models})

def _parse(value):
    return _parse_reduce(value[1:]) if _startswith(value, '$') else value

def _to_fields(props, model_store=models):
    """Maps YAML props dictionary into class fields
    """
    return {
        name: field(*(attrs.get('args', ())), **{
            key: value
            for key, value in attrs.items() if key not in ['type', 'args']
        })
        for name, field, attrs in (
            (name, getattr(model_store, attrs['type']), attrs)
            for name, attrs in {
                key: {
                    k: _parse(v)
                    for k, v in values.items()
                }
                for key, values in props.items()
            }.items()
        ) if name[:2] != '__' and issubclass(field, models.Field)
    }

def _each(iterable, accept, unpack=False, **kwargs):
    _ = (
        [accept(item, **kwargs) for item in iterable] if not unpack else
        [accept(*item, **kwargs) for item in iterable]
    )

_ueach = partial(_each, unpack=True)

def augment(path, cls):
    if not issubclass(cls, models.Model):
        raise ValueError('yodl decorator needs to be applied to a Django model')

    with open(path, 'r') as handle:
        fields = _to_fields(yaml.load(handle.read(), Loader=yaml.FullLoader))

    _ueach(fields.items(), cls.add_to_class)
