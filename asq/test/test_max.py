import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestMax(unittest.TestCase):

    def test_max(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).max()
        self.assertEqual(b, 9)

    def test_max_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        b = Queryable(a).max(abs)
        self.assertEqual(b, 13)

    def test_max_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).max())

  