""" I/O toolset
"""

import yaml

from django.db.models.query_utils import DeferredAttribute

from exos import extend

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

ATTRIBUTES = {
    'CharField': {
        'max_length': 'max_length',
        'unique': lambda f: f.unique
    },
    'IntegerField': {
        'default': 'default'
    },
    'DateTimeField': {
        'args': lambda f: [f.verbose_name]
    },
    'ForeignKey': {
        'on_delete': lambda f: '$models.{}'.format(f.remote_field.on_delete.__name__),
        'args': lambda f: [f.remote_field.model.__name__]
    },
}


def deconstruct(instance, schema):
    kind = type(instance).__name__
    return extend(
        {'type': kind},
        {
            k: v(instance) if callable(v) else instance.__dict__[v]
            for k, v in schema[kind].items()
        }
    )


_deid = lambda k: k[:-3] if k[-3:] == '_id' else k


def yodlify(cls, schema=ATTRIBUTES):
    fields = {
        name: attr.field  # django 3!
        for name, attr in cls.__dict__.items()
        if isinstance(attr, DeferredAttribute) and name != 'id'
    }

    return yaml.dump({
        _deid(name): deconstruct(field, schema)
        for name, field in fields.items()
    })
