"""utility module for the yodl package
"""

from functools import reduce, partial
import yaml
from exos import ueach

from django.db import models

__author__ = "Bruno Lange"
__email__ = "blangeram@gmail.com"
__license__ = "MIT"


def _startswith(obj, prefix):
    return isinstance(obj, str) and obj[: len(prefix)] == prefix


def _navigate(acc, curr):
    return acc[curr] if isinstance(acc, dict) else getattr(acc, curr)


def _parse_reduce(value):
    return reduce(_navigate, value.split("."), {"models": models})


def _parse(value):
    return _parse_reduce(value[1:]) if _startswith(value, "$") else value


def _map_values(fun, dic):
    return {k: fun(v) for k, v in dic.items()}


def _filter_keys(predicate, dic):
    return {k: v for k, v in dic.items() if predicate(k)}


def _not_in(collection):
    return lambda x: x not in collection


def _to_fields(props, model_store=models):
    """Maps YAML props dictionary into class fields"""
    return {
        name: field(*args, **kwargs)
        for name, field, args, kwargs in (
            (
                name,
                getattr(model_store, attrs["type"]),
                attrs.get("args", ()),
                _filter_keys(_not_in({"type", "args"}), attrs),
            )
            for name, attrs in _map_values(partial(_map_values, _parse), props).items()
        )
        if name[:2] != "__" and issubclass(field, models.Field)
    }


def augment(path, cls):
    if not issubclass(cls, models.Model):
        raise ValueError("yodl decorator needs to be applied to a Django model")

    with open(path, "r") as handle:
        fields = _to_fields(yaml.load(handle.read(), Loader=yaml.FullLoader))

    ueach(cls.add_to_class, fields.items())
