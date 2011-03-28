__author__ = 'Robert Smallshire'

class Record(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
        self.__dict__ = self

def new(**kwargs):
    return Record(**kwargs)


