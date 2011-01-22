class Grouping(object):
    '''A proxy for a particular value sequence in an OrderedDict, including its key.'''

    def __init__(self, ordereddict, key):
        '''
        Args:
            ordereddict: An ordereddict with indexable and iterable values
        '''
        self._sequence = ordereddict[key]
        self._key = key

    key = property(lambda self: self._key)

    def __iter__(self):
        return iter(self._sequence)

    def __getitem__(self, index):
        return self._sequence[index]

    def __len__(self):
        return len(self._sequence)

    def __contains__(self, item):
        return item in self._sequence

