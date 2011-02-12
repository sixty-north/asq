import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestMin(unittest.TestCase):

    def test_min(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min()
        self.assertEqual(b, -8)

    def test_min_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min(abs)
        self.assertEqual(b, 1)

    def test_min_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).min())

    def test_min_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.min())