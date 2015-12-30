"""This module contains the definition of the IndexedElement type.
"""

from collections import namedtuple

IndexedElement = namedtuple('IndexedElement', ['index', 'element'])

CorrespondingArgumentValue = namedtuple('CorrespondingArgumentValue', ['arg', 'value'])

