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
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        sys.stderr.write('Could not import OrderedDict. For Python versions earlier than 2.7 install the')
        sys.stderr.write('ordereddict module from the Python Package Index with easy_install ordereddict.')
        sys.exit(1)



  