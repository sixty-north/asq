import unittest
from asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestFirstOrDefault(unittest.TestCase):

    def test_first_or_default(self):
        a = [42, 45, 23, 12]
        b = Queryable(a).first_or_default(37)
        self.assertEqual(b, 42)

    def test_first_or_default_empty(self):
        a = []
        b = Queryable(a).first_or_default(37)
        self.assertEqual(b, 37)

    def test_first_or_default_infinite(self):
        b = Queryable(infinite()).first_or_default(37)
        self.assertEqual(b, 0)

    def test_first_or_default_predicate(self):
        a = [37, 54, 23, 12]
        b = Queryable(a).first_or_default(78, lambda x: x >= 50)
        self.assertEqual(b, 54)

    def test_first_or_default_predicate_empty(self):
        a = []
        b = Queryable([]).first_or_default(56, lambda x: x >= 50)
        self.assertEqual(b, 56)

    def test_first_predicate_missing(self):
        a = [37, 42, 23, 12]
        b = Queryable(a).first_or_default(98, lambda x: x >= 50)
        self.assertEqual(b, 98)

    def test_first_predicate_not_callable(self):
        a = [37, 42, 23, 12]
        self.assertRaises(TypeError, lambda: Queryable(a).first_or_default(98, "not callable"))

    def test_first_or_default_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.first_or_default(37))
