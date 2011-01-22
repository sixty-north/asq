import sys
from asq.grouping import Grouping

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        sys.stderr.write('Could not import OrderedDict. For Python versions earlier than 2.7 install the')
        sys.stderr.write('ordereddict module from the Python Package Index with easy_install ordereddict.')
        sys.exit(1)

class Lookup(object):
    '''An ordered dictionary for which there can be multiple value for each key.'''

    def __init__(self):
        self._dict = OrderedDict()

    def __setitem__(self, key, value):
        if key not in self._dict:
            self._dict[key] = []
        self._dict[key].append(value)

    def __getitem__(self, key):
        '''The sequence corresponding to a given key.'''
        return Grouping(self._dict, key)

    def __iter__(self):
        '''An iterator over Groupings in the lookup.'''
        for key in self._dict.keys():
            yield Grouping(self._dict, key)

    def __len__(self):
        '''The number of groupings (keys) in the lookup.'''
        return len(self._dict)

    