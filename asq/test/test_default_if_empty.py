import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import infinite

__author__ = 'rjs'

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

    def test_default_if_empty_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.default_if_empty(5))
