

from . import utils as u

def yodl(arg):
    if isinstance(arg, type):
        u.augment('{}.yaml'.format(arg.__name__), arg)
        return arg

    def wrap(cls):
        u.augment(arg, cls)
        return cls
    return wrap
