import unittest
from src.asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestEqualOperator(unittest.TestCase):

    def test_eq_positive(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a) == b
        self.assertTrue(c)

    def test_eq_negative(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a) == b
        self.assertFalse(c)

    def test_eq_shorter_longer(self):
        a = [1, 2, 3]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a) == b
        self.assertFalse(c)

    def test_eq_longer_shorter(self):
         a = [1, 2, 3, 4, 5, 6]
         b = (1, 2, 3)
         c = Queryable(a) == b
         self.assertFalse(c)

    def test_eq_empty(self):
        a = []
        b = ()
        c = Queryable(a) == b
        self.assertTrue(c)

    def test_eq_non_iterable(self):
        a = [1, 2, 3]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a) == b)

    def test_eq_order(self):
        a = [1, 2]
        b = (2, 1)
        c = Queryable(a) == b
        self.assertFalse(c)

    def test_eq_finite_infinite(self):
        a = infinite()
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a) == b
        self.assertFalse(c)

    def test_eq_infinite_finite(self):
        a = (1, 2, 3, 5, 16, 32)
        b = infinite()
        c = Queryable(a) == b
        self.assertFalse(c)

    def test_eq_closed(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a)
        c.close()
        self.assertRaises(ValueError, lambda: c == b)

class TestNotEqualOperator(unittest.TestCase):

    def test_ne_negative(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a) != b
        self.assertFalse(c)

    def test_ne_positive(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a) != b
        self.assertTrue(c)

    def test_ne_shorter_longer(self):
        a = [1, 2, 3]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a) != b
        self.assertTrue(c)

    def test_ne_longer_shorter(self):
         a = [1, 2, 3, 4, 5, 6]
         b = (1, 2, 3)
         c = Queryable(a) != b
         self.assertTrue(c)

    def test_ne_empty(self):
        a = []
        b = ()
        c = Queryable(a) != b
        self.assertFalse(c)

    def test_ne_non_iterable(self):
        a = [1, 2, 3]
        b = None
        self.assertRaises(TypeError, lambda: Queryable(a) != b)

    def test_ne_order(self):
        a = [1, 2]
        b = (2, 1)
        c = Queryable(a) != b
        self.assertTrue(c)

    def test_ne_finite_infinite(self):
        a = infinite()
        b = (1, 2, 3, 5, 16, 32)
        c = Queryable(a) != b
        self.assertTrue(c)

    def test_ne_infinite_finite(self):
        a = (1, 2, 3, 5, 16, 32)
        b = infinite()
        c = Queryable(a) != b
        self.assertTrue(c)

    def test_ne_closed(self):
        a = [1, 2, 3, 4, 16, 32]
        b = (1, 2, 3, 4, 16, 32)
        c = Queryable(a)
        c.close()
        self.assertRaises(ValueError, lambda: c != b)

