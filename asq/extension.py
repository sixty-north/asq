'''Adding extension operators.'''

__author__ = 'Robert Smallshire'

from ._portability import function_name

# TODO: [asq 1.0] extension needs unit tests

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
    '''
    # Should we be using functools.update_wrapper in here?
    if name is None:
        name = function_name(function)
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
    '''
    def decorator(f):
        return add_method(f, klass, name)
    return decorator




