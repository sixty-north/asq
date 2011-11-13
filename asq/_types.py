'''
Predicate functions for testing Python objects to determine their type.
'''
from asq import _portability

__author__ = "Robert Smallshire"

def is_iterable(obj):
    '''Determine if an object is iterable.

    Args:
        obj: The object to be tested for supporting iteration.

    Returns:
        True if the object is iterable, otherwise False.
    '''
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def is_type(obj):
    '''Determine if an object is a type.

    Args:
        obj: The object to be tested for being a type, or a tuple of types.

    Returns:
        True if the object is a type or tuple of types, otherwise False.
    '''
    try:
        isinstance(None, obj)
        return True
    except TypeError:
        return False

# TODO: Put is_callable in here too.

# TODO: is_string
def is_string(obj):
    return _portability.is_string(obj)

# TODO: is_integer


