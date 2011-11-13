import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

class TestMax(unittest.TestCase):

    def test_max(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).max()
        self.assertEqual(b, 9)

    def test_max_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        b = Queryable(a).max(abs)
        self.assertEqual(b, 13)

    def test_max_selector_not_callable(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        self.assertRaises(TypeError, lambda: Queryable(a).max("not callable"))
        
    def test_max_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).max())

    def test_max_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.max())