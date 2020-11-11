"""decorators module
"""

from . import utils as u

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'


def yodl(arg):
    if isinstance(arg, type):
        u.augment('{}.yaml'.format(arg.__name__), arg)
        return arg

    path = arg
    def wrap(cls):
        u.augment(path, cls)
        return cls
    return wrap
