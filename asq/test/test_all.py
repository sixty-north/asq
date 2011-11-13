import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

class TestAll(unittest.TestCase):

    def test_all_positive(self):
        a = [True, True, True, True]
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_negative(self):
        a = [True, True, True, False]
        b = Queryable(a).all()
        self.assertFalse(b)

    def test_all_default_predicate_positive(self):
        a = [1, 1, 1, 1]
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_default_predicate_negative(self):
        a = [1, 1, 1, 0]
        b = Queryable(a).all()
        self.assertFalse(b)

    def test_all_predicate_positive(self):
        a = [10, 13, 25, 14]
        b = Queryable(a).all(lambda x: x >= 10)
        self.assertTrue(b)

    def test_all_predicate_negative(self):
        a = [10, 13, 25, 8]
        b = Queryable(a).all(lambda x: x >= 10)
        self.assertFalse(b)

    def test_all_empty(self):
        a = []
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_predicate_non_callable(self):
        a = [True, True, True]
        self.assertRaises(TypeError, lambda: Queryable(a).all("not callable"))

    def test_all_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.all())