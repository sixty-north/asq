import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

__author__ = "Sixty North"

class TestDefaultIfEmpty(unittest.TestCase):

    def test_default_if_empty_empty(self):
        b = Queryable([]).default_if_empty(5).to_list()
        self.assertEqual(b, [5])

    def test_default_if_empty_non_empty(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).default_if_empty(42).to_list()
        self.assertEqual(b, a)

    def test_default_if_empty_infinite(self):
        b = Queryable(infinite()).default_if_empty(42).take(5).to_list()
        self.assertEqual(b, [0, 1, 2, 3, 4])

    def test_default_if_empty_is_deferred_not_empty(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).default_if_empty(42)
        self.assertEqual(a.trace, [])
        c = b.take(3).to_list()
        self.assertEqual(a.trace, [0, 1, 2])

    def test_default_if_empty_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.default_if_empty(5))
