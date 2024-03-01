import unittest
from asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestReverse(unittest.TestCase):

    def test_reverse(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).reverse().to_list()
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)

    def test_reverse_non_sequence(self):
        a = infinite()
        b = Queryable(a).take(10).reverse().to_list()
        c = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.assertEqual(b, c)

    def test_reverse_closed(self):
        b = Queryable([1, 2, 4, 8])
        b.close()
        self.assertRaises(ValueError, lambda: b.reverse())

    def test_reverse_empty(self):
        a = []
        b = Queryable(a).reverse().to_list()
        c = []
        self.assertEqual(a, c)