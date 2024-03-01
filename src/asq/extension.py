'''Adding extension operators.'''

__author__ = 'Sixty North'

from ._portability import function_name


def add_method(function, klass, name=None):
    '''Add an existing function to a class as a method.

    Note: Consider using the extend decorator as a more readable alternative
        to using this function directly.

    Args:
        function: The function to be added to the class klass.

        klass: The class to which the new method will be added.

        name: An optional name for the new method.  If omitted or None the
            original name of the function is used.

    Returns:
        The function argument unmodified.

    Raises:
        ValueError: If klass already has an attribute with the same name as the
            extension method.
    '''
    # Should we be using functools.update_wrapper in here?
    if name is None:
        name = function_name(function)
    if hasattr(klass, name):
        raise ValueError("Cannot replace existing attribute with method "
                         "'{name}'".format(name=name))
    setattr(klass, name, function)
    return function


def extend(klass, name=None):
    '''A function decorator for extending an existing class.

    Use as a decorator for functions to add to an existing class.

    Args:
        klass: The class to be decorated.

        name: The name the new method is to be given in the klass class.

    Returns:
        A decorator function which accepts a single function as its only
        argument.  The decorated function will be added to class klass.

    Raises:
        ValueError: If klass already has an attribute with the same name as the
            extension method.
    '''
    def decorator(f):
        return add_method(f, klass, name)

    return decorator
