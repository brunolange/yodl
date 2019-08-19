"""
"""
import yaml

from django.db.models.query_utils import DeferredAttribute

from .utils import extend

ATTRIBUTES = {
    'CharField': {
        'max_length': 'max_length'
    },
    'IntegerField': {
        'default': 'default'
    },
    'DateTimeField': {
        'args': lambda f: [f.verbose_name]
    },
    'ForeignKey': {
        'on_delete': lambda f: '$models.{}'.format(f.remote_field.on_delete.__name__)
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

def yodlify(cls, schema=ATTRIBUTES):
    fields = {
        name: attr.field # django 3!
        for name, attr in cls.__dict__.items()
        if isinstance(attr, DeferredAttribute)
        and name != 'id'
    }

    return yaml.dump({
        name: deconstruct(field, schema)
        for name, field in fields.items()
    })
