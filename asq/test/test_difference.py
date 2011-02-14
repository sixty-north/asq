import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestDifference(unittest.TestCase):

    def test_difference(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).difference(b).to_list()
        d = [1, 3, 5, 6, 7, 8]
        self.assertEqual(c, d)

    def test_difference_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).difference(b))

    def test_difference_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).difference(b).to_list()
        d = [1, 2, 3, 4, 5]
        self.assertEqual(c, d)

    def test_difference_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, 8]
        c = Queryable(a).difference(b, abs).to_list()
        d = [1, 3, 6, 7]
        self.assertEqual(c, d)

    def test_difference_selector_non_callable(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, 8]
        self.assertRaises(TypeError, lambda: Queryable(a).difference(b, "not callable"))

    def test_difference_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).difference(b).take(10).to_list()
        d = [0, 1, 4, 5, 6, 8, 11, 12, 13, 14]
        self.assertEqual(c, d)

    def test_difference_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).difference(b)
        self.assertEqual(a.trace, [])
        d = c.take(10).to_list()
        e = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.assertEqual(a.trace, e)

    def test_difference_distinct(self):
        a = [1, 1, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).difference(b).to_list()
        d = [1, 4, 3]
        self.assertEqual(c, d)

    def test_difference_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.difference([2, 5]))
        