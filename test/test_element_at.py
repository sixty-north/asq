import unittest
from src.asq.queryables import Queryable
from helpers import infinite

__author__ = "Sixty North"

class TestElementAt(unittest.TestCase):

    def test_element_at(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        b = Queryable(a).element_at(3)
        self.assertEqual(b, 8)

    def test_element_at_out_of_range_infinite(self):
        self.assertRaises(ValueError, lambda: Queryable(infinite()).element_at(-1))

    def test_element_at_out_of_range(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        self.assertRaises(ValueError, lambda: Queryable(a).element_at(20))

    def test_element_at_out_of_range_non_sequence(self):
        def series():
            yield 1
            yield 2
            yield 4
            yield 8
        a = series()
        self.assertRaises(ValueError, lambda: Queryable(a).element_at(20))

    def test_element_at_infinite(self):
        b = Queryable(infinite()).element_at(5)
        self.assertEqual(b, 5)

    def test_element_at_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.element_at(0))
