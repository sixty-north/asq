import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestLastOrDefault(unittest.TestCase):

    def test_last_or_default(self):
        a = [42, 45, 23, 12]
        b = Queryable(a).last_or_default(37)
        self.assertEqual(b, 12)

    def test_last_or_default_empty(self):
        a = []
        b = Queryable(a).last_or_default(37)
        self.assertEqual(b, 37)

    def test_last_or_default_predicate(self):
        a = [37, 54, 57, 23, 12]
        b = Queryable(a).last_or_default(12, lambda x: x >= 50)
        self.assertEqual(b, 57)

    def test_last_or_default_predicate_empty(self):
        a = []
        b = Queryable(a).last_or_default(12, lambda x: x >= 50)
        self.assertEqual(b, 12)

    def test_last_or_default_predicate_missing(self):
        a = [37, 42, 23, 12]
        b = Queryable(a).last_or_default(78, lambda x: x >= 50)
        self.assertEqual(b, 78)

    def test_last_or_default_predicate_not_callable(self):
        a = [37, 54, 57, 23, 12]
        self.assertRaises(TypeError, lambda: Queryable(a).last_or_default(12, "not callable"))
        
    def test_last_or_default_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.last_or_default(37))
