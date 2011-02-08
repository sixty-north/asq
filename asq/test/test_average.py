import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestAverage(unittest.TestCase):

    def test_average(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 3]
        b = Queryable(a).average()
        self.assertEqual(b, 2)

    def test_average_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).average(abs)
        self.assertEqual(b, 5)

    def test_average_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).average())
