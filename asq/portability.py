'''Python 2 and Python 3 compatibility'''

__author__ = 'rjs'

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
        sys.stderr.write('Could not import OrderedDict. For Python versions earlier than 2.7 install the')
        sys.stderr.write('ordereddict module from the Python Package Index with easy_install ordereddict.')
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
    # Python 2
    is_callable = callable
except NameError:
    from collections import Callable
    def is_callable(x):
        return isinstance(x, Callable)


    


  