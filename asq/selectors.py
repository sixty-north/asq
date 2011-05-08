'''Selector functions and selector function factories.'''

__author__ = 'Robert Smallshire'


def k_(key):
    '''Create a selector function which indexes into the element by key.

    Args:
        key: The key which the generated selector will use to index into
            elements.

    Returns:
        A unary selector function which indexes into its only argument with
        the key value.
    '''
    return lambda element: element[key]


def a_(name):
    '''Create a selector function which selects an attribute by name.

    Args:
        name: The name of the attribute which will be retrieved from each
            element.

    Returns:
        A unary selector function which retrieves the named attribute from its
        only argument and returns the value of that attribute.
    '''
    return lambda element: getattr(element, name)


def m_(name, *args, **kwargs):
    '''Create a selector function which calls a named method.

    Args:
        name: The name of the method which will be called on each element.

        *args: Any optional positional arguments which will be passed to the
            called method.

        **kwargs: Any optional named arguments which will be passed to the
            called method.

    Returns:
        A unary selector function which calls the named method with any
        optional positional or named arguments and which returns the
        result of the method call.
    '''
    return lambda element: getattr(element, name)(*args, **kwargs)


def identity(x):
    '''The identity function.

    The identity function returns its only argument.

    Args:
        x: A value that will be returned.

    Returns:
        The argument x.
    '''
    return x
