import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestContains(unittest.TestCase):

    def test_contains_positive(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(2)
        self.assertTrue(b)

    def test_contains_negative(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(6)
        self.assertFalse(b)

    # TODO: test_contains_infinite_positive

    def test_contains_empty(self):
        b = Queryable([]).contains(7)
        self.assertFalse(b)

    def test_contains_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.contains(5))


  