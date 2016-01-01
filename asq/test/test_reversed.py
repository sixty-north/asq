import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite

__author__ = "Sixty North"

class TestReversed(unittest.TestCase):

    def test_reversed(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = list(reversed(Queryable(a)))
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)

    def test_reversed_non_sequence(self):
        a = infinite()
        b = list(reversed(Queryable(a).take(10)))
        c = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.assertEqual(b, c)

    def test_reversed_closed(self):
        b = Queryable([1, 2, 4, 8])
        b.close()
        self.assertRaises(ValueError, lambda: reversed(b))

    def test_reversed_empty(self):
        a = []
        b = list(reversed(Queryable(a)))
        c = []
        self.assertEqual(a, c)