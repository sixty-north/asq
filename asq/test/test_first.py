import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite

__author__ = 'rjs'

class TestFirst(unittest.TestCase):

    def test_first(self):
        a = [42, 45, 23, 12]
        b = Queryable(a).first()
        self.assertEqual(b, 42)

    def test_first_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).first())

    def test_first_infinite(self):
        b = Queryable(infinite()).first()
        self.assertEqual(b, 0)

    def test_first_predicate(self):
        a = [37, 54, 57, 23, 12]
        b = Queryable(a).first(lambda x: x >= 50)
        self.assertEqual(b, 54)

    def test_first_predicate_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).first(lambda x: x >= 50))
        
    def test_first_predicate_missing(self):
        a = [37, 42, 23, 12]
        self.assertRaises(ValueError, lambda: Queryable(a).first(lambda x: x >= 50))

    def test_first_predicate_not_callable(self):
        a = [37, 54, 57, 23, 12]
        self.assertRaises(TypeError, lambda: Queryable(a).first("not callable"))

    def test_first_predicate_infinite(self):
        a = infinite()
        b = Queryable(a).first(lambda x: x >= 50)
        self.assertEqual(b, 50)

    def test_first_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.first())
