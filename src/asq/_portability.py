'''Python 2 and Python 3 compatibility'''

__author__ = "Sixty North"

import sys

try:
    # Python 2
    from itertools import imap
except ImportError:
    # Python 3
    imap = map

try:
    # Python 2
    from itertools import ifilter
except ImportError:
    # Python 3
    ifilter = filter

try:
    # Python 2
    from itertools import izip
except ImportError:
    # Python 3
    izip = zip

try:
    # Python 2
    from itertools import izip_longest
except ImportError:
    # Python 3
    from itertools import zip_longest as izip_longest

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        sys.stderr.write('Could not import OrderedDict. For Python versions '
                         'earlier than 2.7 install the')
        sys.stderr.write('ordereddict module from the Python Package Index '
                         'with easy_install ordereddict.')
        sys.exit(1)

try:
    # Python 2
    irange = xrange
except NameError:
    #Python 3
    irange = range


try:
    # Python 2
    fold = reduce
except NameError:
    import functools
    fold = functools.reduce

try:
    # Python 2.x and Python 3.2+
    is_callable = callable
except NameError:
    # Python 3.0 and Python 3.1
    from collections import Callable

    def is_callable(x):
        return isinstance(x, Callable)

try:
    # Python 3
    def _dummy():
        pass

    _dummy.__name__
    del _dummy

    def function_name(f):
        return f.__name__
except AttributeError:
    # Python 2
    def function_name(f):
        return f.func_name

try:
    # Python 2
    unicode()

    def has_unicode_type():
        return True

except NameError:
    # Python 3
    def has_unicode_type():
        return False

def itervalues(dictionary):
    '''Get an iterator over dictionary values.

    Attempts to avoid copying the dictionary values.

    Args:
        dictionary: The dictionary for which an iterator over values is wanted.

    Returns:
        An iterator over the dictionary values.
    '''
    try:
        return dictionary.itervalues()
    except AttributeError:
        pass
    return iter(dictionary.values())

def iteritems(dictionary):
    '''Get an iterator over dictionary items.

    Attempts to avoid copying the dictionary items.

    Args:
        dictionary: The dictionary for which an iterator over items is wanted.

    Returns:
        An iterator over the dictionary items.
    '''
    try:
        return dictionary.iteritems()
    except AttributeError:
        pass
    return iter(dictionary.items())

try:
    # Python 2.7+ and Python 3.2+
    from functools import total_ordering as totally_ordered
except ImportError:
    # Python 2.6 version from
    # http://code.activestate.com/recipes/576685-total-ordering-class-decorator/
    # This recipe doesn't actually work on Python 3.0 or 3.1 but that doesn't
    # matter since neither of those implementations cause the
    # extra methods added by the decorator to be exercised.  This may become
    # an issue in future if somebody creates an alternative Python 3
    # implementation which is not up to Python 3.2 completeness.  That seems
    # unlikely.
    def totally_ordered(cls):
        'Class decorator that fills-in missing ordering methods'
        convert = {
            '__lt__': [('__gt__', lambda self, other: other < self),
                       ('__le__', lambda self, other: not other < self),
                       ('__ge__', lambda self, other: not self < other)],
            '__le__': [('__ge__', lambda self, other: other <= self),
                       ('__lt__', lambda self, other: not other <= self),
                       ('__gt__', lambda self, other: not self <= other)],
            '__gt__': [('__lt__', lambda self, other: other > self),
                       ('__ge__', lambda self, other: not other > self),
                       ('__le__', lambda self, other: not self > other)],
            '__ge__': [('__le__', lambda self, other: other >= self),
                       ('__gt__', lambda self, other: not other >= self),
                       ('__lt__', lambda self, other: not self >= other)]
        }
        if hasattr(object, '__lt__'):
            roots = [op for op in convert if getattr(cls, op) is not getattr(object, op)]
        else:
            roots = set(dir(cls)) & set(convert)
        assert roots, 'must define at least one ordering operation: < > <= >='
        root = max(roots)       # prefer __lt __ to __le__ to __gt__ to __ge__
        for opname, opfunc in convert[root]:
            if opname not in roots:
                opfunc.__name__ = opname
                opfunc.__doc__ = getattr(int, opname).__doc__
                setattr(cls, opname, opfunc)
        return cls

try:
    # Python 2
    basestring
    def is_string(s):
        return isinstance(s, basestring)
except NameError:
    # Python 3
    def is_string(s):
        return isinstance(s, str)

        
