"""This module contains the definition of the IndexedElement type.
"""

from collections import namedtuple

IndexedElement = namedtuple('IndexedElement', ['index', 'value'])

KeyedElement = namedtuple('KeyedElement', ['key', 'value'])

