'''
test_queryable.py Unit tests for asq.queryable.Queryable
'''
import unittest

from asq.queryable import Queryable

def times_two(x):
    return 2 * x

def times(x, y):
    return x * y

def infinite():
    i = 0
    while True:
        yield i
        i += 1

class TracingGenerator(object):

    def __init__(self):
        self._trace = []
        self._i = 0

    def __iter__(self):
        while True:
            self._trace.append(self._i)
            yield self._i
            self._i += 1

    trace = property(lambda self: self._trace)

class TestQueryable(unittest.TestCase):

    def test_non_iterable(self):
        self.assertRaises(TypeError, lambda: Queryable(5))

def inc_chr(y):
    return chr(ord(y)+1)

def randgen():
    import random
    while True:
        yield random.random()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueryable)
    unittest.TextTestRunner(verbosity=2).run(suite)
