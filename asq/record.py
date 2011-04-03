__author__ = 'Robert Smallshire'

class Record(object):
    '''A class to which any attribute can be added at construction.'''

    def __init__(self, **kwargs):
        '''Initialise a Record with an attribute for each keyword argument.

        The attributes of a Record are mutable and may be read from and written
        to using regular Python instance attribute syntax.

        Args:
            **kwargs: Each keyword argument will be used to initialise an
                attribute with the same name as the argument and the given
                value.
        '''
        self.__dict__.update(kwargs)

    def __getstate__(self):
        '''Support for pickling.'''
        return self

    def __setstate__(self, state):
        '''Support for unpickling.'''
        self.update(state)
        self.__dict__ = self

    def __str__(self):
        '''A string representation of the Record.'''
        return "Record(" + ', '.join(str(key) + '=' + str(value) for key, value in self.__dict__.items()) + ')'

    def __repr__(self):
        '''A valid Python expression string representation of the Record.'''
        return "Record(" + ', '.join(str(key) + '=' + repr(value) for key, value in self.__dict__.items()) + ')'

def new(**kwargs):
    '''A convenience factory for creating Records.

    Args:
        **kwargs: Each keyword argument will be used to initialise an
            attribute with the same name as the argument and the given
            value.

    Returns:
        A Record which has a named attribute for each of the keyword arguments.
    '''
    return Record(**kwargs)



