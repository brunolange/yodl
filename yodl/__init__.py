"""yodl!
yodl provides a class decorator to build django models
from YAML configuration files
"""

from .decorators import yodl
from .io import yodlify

__author__ = 'Bruno Lange'
__email__ = 'blangeram@gmail.com'
__license__ = 'MIT'

__all__ = ['yodl', 'yodlify']
