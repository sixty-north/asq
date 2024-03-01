import unittest
from asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestContains(unittest.TestCase):

    def test_contains_positive(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(2)
        self.assertTrue(b)

    def test_contains_negative(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(6)
        self.assertFalse(b)

    def test_contains_infinite(self):
        a = infinite()
        b = Queryable(a).contains(37)
        self.assertTrue(b)

    def test_contains_non_sequence_positive(self):
        def series():
            yield 5
            yield 7
            yield -3
            yield 2
        a = series()
        b = Queryable(a).contains(2)
        self.assertTrue(b)

    def test_contains_non_sequence_negative(self):
        def series():
            yield 5
            yield 7
            yield -3
            yield 2
        a = series()
        b = Queryable(a).contains(6)
        self.assertFalse(b)

    def test_contains_empty(self):
        b = Queryable([]).contains(7)
        self.assertFalse(b)

    def test_contains_comparer1(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(15, lambda a, b: abs(a) == abs(b))
        self.assertTrue(b)

    def test_contains_comparer2(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(-9, lambda a, b: abs(a) == abs(b))
        self.assertTrue(b)

    def test_contains_comparer3(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        b = Queryable(a).contains(4, lambda a, b: abs(a) == abs(b))
        self.assertFalse(b)

    def test_contains_non_callable_comparator(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -15, 7]
        self.assertRaises(TypeError, lambda: Queryable(a).contains(-9, "not callable"))

    def test_contains_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.contains(5))


