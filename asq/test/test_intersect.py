import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestIntersect(unittest.TestCase):

    def test_intersect(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).intersect(b).to_list()
        d = [2, 4]
        self.assertEqual(c, d)

    def test_intersect_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).intersect(b))

    def test_intersect_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).intersect(b).to_list()
        d = []
        self.assertEqual(c, d)

    def test_intersect_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, 8]
        c = Queryable(a).intersect(b, abs).to_list()
        d = [2, 4, -5, -8]
        self.assertEqual(c, d)

    def test_intersect_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).intersect(b).take(5).to_list()
        d = [2, 3, 7, 9, 10]
        self.assertEqual(c, d)

    def test_intersect_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).intersect(b)
        self.assertEqual(a.trace, [])
        d = c.take(5).to_list()
        e = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(a.trace, e)

    def test_intersect_distinct(self):
        a = [1, 1, 2, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).intersect(b).to_list()
        d = [2, 5]
        self.assertEqual(c, d)

  