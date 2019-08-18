"""yodl!
yodl provides a class decorator to build django models
from YAML configuration files
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

def _to_fields(props, model_store=models, **methods):
    """Maps YAML props dictionary into class fields
    """
    return _extend({
        name: field(*(attrs.get('args', ())), **{
            key: value
            for key, value in attrs.items() if key not in ['type', 'args']
        })
        for name, field, attrs in (
            (name, getattr(model_store, attrs['type']), attrs)
            for name, attrs in props.items()
        ) if name[:2] != '__'
    }, methods)

def _each(iterable, accept, unpack=False):
    _ = (
        [accept(item) for item in iterable] if not unpack else
        [accept(*item) for item in iterable]
    )

_ueach = partial(_each, unpack=True)

def _augment(path, klass):
    with open(path, 'r') as handle:
        fields = _to_fields(yaml.load(handle.read(), Loader=yaml.FullLoader))

    _ueach(fields.items(), klass.add_to_class)

def yodl(arg):
    if isinstance(arg, type):
        _augment('{}.yaml'.format(arg.__name__), arg)
        return arg

    def wrap(klass):
        _augment(arg, klass)
        return klass
    return wrap
