import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestUnion(unittest.TestCase):

    def test_union(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = [2, 4, 9, 11]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        self.assertEqual(c, d)

    def test_union_non_iterable(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a).union(b))

    def test_union_disjoint(self):
        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8, 9, 10]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(c, d)

    def test_union_selector(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, -9]
        c = Queryable(a).union(b, abs).to_list()
        d = [1, 2, 3, 4, -5, 6 , 7, -8, -9]
        self.assertEqual(c, d)

    def test_union_selector_not_callable(self):
        a = [1, 2, 3, 4, -5, 6, 7, -8]
        b = [-2, -4, 5, -9]
        self.assertRaises(TypeError, lambda: Queryable(a).union(b, "not callable"))

    def test_union_infinite(self):
        b = [3, 7, 2, 9, 10]
        c = Queryable(infinite()).union(b).take(5).to_list()
        d = [0, 1, 2, 3, 4]
        self.assertEqual(c, d)

    def test_union_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = [3, 7, 2, 9, 10]
        c = Queryable(a).union(b)
        self.assertEqual(a.trace, [])
        d = c.take(5).to_list()
        e = [0, 1, 2, 3, 4]
        self.assertEqual(a.trace, e)

    def test_union_distinct(self):
        a = [1, 1, 2, 2, 4, 5, 3]
        b = [2, 5, 5]
        c = Queryable(a).union(b).to_list()
        d = [1, 2, 4, 5, 3]
        self.assertEqual(c, d)

    def test_union_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.union([1, 2, 3]))
