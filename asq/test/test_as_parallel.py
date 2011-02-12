import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestAsParallel(unittest.TestCase):

    def test_as_parallel_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.as_parallel())