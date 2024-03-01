import unittest
from asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestDistinct(unittest.TestCase):

    def test_distinct(self):
        a = [5, 7, -3, 2, 1, 5, 3, 2, 1, -15, 7]
        b = Queryable(a).distinct().to_list()
        c = [5, 7, -3, 2, 1, 3, -15]
        self.assertEqual(b, c)

    def test_distinct_selector(self):
        a = [5, 7, -3, 2, 1, 5, 3, 2, 1, -15, 7]
        b = Queryable(a).distinct(abs).to_list()
        c = [5, 7, -3, 2, 1, -15]
        self.assertEqual(b, c)

    def test_distinct_selector_non_callable(self):
        a = [5, 7, -3, 2, 1, 5, 3, 2, 1, -15, 7]
        self.assertRaises(TypeError, lambda: Queryable(a).distinct("not callable"))

    def test_distinct_empty(self):
        b = Queryable([]).distinct().to_list()
        self.assertEqual(b, [])

    def test_distinct_infinite(self):
        b = Queryable(infinite()).distinct().take(5).to_list()
        c = [0, 1, 2, 3, 4]
        self.assertEqual(b, c)

    def test_distinct_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.distinct())