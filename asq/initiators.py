'''Initiators are factory functions for creating Queryables.'''
import itertools

from ._portability import irange
from asq._portability import is_callable

__author__ = 'Robert Smallshire'


def query(iterable):
    '''Make an iterable queryable.

    Use this function as an entry-point to the asq system of chainable query
    methods.

    Note: Currently this factory only provides support for objects supporting
        the iterator protocol.  Future implementations may support other
        providers.

    Args:
        iterable: Any object supporting the iterator protocol.

    Returns:
        An instance of Queryable.

    Raises:
        TypeError: If iterable is not actually iterable
    '''
    # Avoid a circular module dependency
    from .queryables import Queryable
    return Queryable(iterable)


def integers(start, count):
    '''Generates in sequence the integral numbers within a range.

    Note: This method uses deferred execution.

    Args:
        start: The first integer in the sequence.
        count: The number of sequential integers to generate.

    Returns:
        A Queryable over the specified range of integers.

    Raises:
        ValueError: If count is negative.
    '''
    if count < 0:
        raise ValueError("integers() count cannot be negative")
    return query(irange(start, start + count))


def repeat(element, count):
    '''Generate a sequence with one repeated value.

    Note: This method uses deferred execution.

    Args:
        element: The value to be repeated.
        count: The number of times to repeat the value.

    Raises:
        ValueError: If the count is negative.
    '''
    if count < 0:
        raise ValueError("repeat() count cannot be negative")
    return query(itertools.repeat(element, count))


_empty = None


def empty():
    '''An empty Queryable.

    Note: The same empty instance will be returned each time.

    Returns: A Queryable over an empty sequence.
    '''
    # We use this lazy initialization of _empty to avoid a circular
    # module dependency
    global _empty
    if _empty is None:
        _empty = query(tuple())
    return _empty


def generate(func, initial):
    if not is_callable(func):
        raise TypeError("func is not callable in call to generate().")
    return query(_generate_result(func, initial))

def _generate_result(func, initial):
    current = initial
    while True:
        yield current
        current = func(current)



