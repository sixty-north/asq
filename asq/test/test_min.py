import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

class TestMin(unittest.TestCase):

    def test_min(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min()
        self.assertEqual(b, -8)

    def test_min_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).min(abs)
        self.assertEqual(b, 1)

    def test_min_selector_not_callable(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        self.assertRaises(TypeError, lambda: Queryable(a).min("not callable"))

    def test_min_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).min())

    def test_min_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.min())