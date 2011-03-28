import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite

__author__ = 'rjs'

class TestAny(unittest.TestCase):

    def test_any_empty(self):
        a = []
        b = Queryable(a).any()
        self.assertFalse(b)

    def test_any_not_empty(self):
        a = [False, False, False]
        b = Queryable(a).any()
        self.assertTrue(b)

    def test_any_negative_predicate(self):
        a = [1, 2, 3, 4, 8, 34]
        b = Queryable(a).any(lambda x: x == 15)
        self.assertFalse(b)

    def test_any_positive_predicate(self):
        a = [1, 2, 3, 4, 8, 34]
        b = Queryable(a).any(lambda x: x == 8)
        self.assertTrue(b)

    def test_any_infinite(self):
        b = Queryable(infinite()).any()
        self.assertTrue(b)

    def test_any_infinite_predicate(self):
        b = Queryable(infinite()).any(lambda x: x == 1000)

    def test_any_predicate_not_callable(self):
        self.assertRaises(TypeError, lambda: Queryable([True]).any("not callable"))

    def test_any_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.any())