import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite

__author__ = "Sixty North"

class TestGetItem(unittest.TestCase):

    def test_getitem(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        b = Queryable(a)[3]
        self.assertEqual(b, 8)

    def test_getitem_out_of_range_infinite(self):
        self.assertRaises(IndexError, lambda: Queryable(infinite())[-1])

    def test_getitem_out_of_range(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        self.assertRaises(IndexError, lambda: Queryable(a)[20])

    def test_getitem_out_of_range_non_sequence(self):
        def series():
            yield 1
            yield 2
            yield 4
            yield 8
        a = series()
        self.assertRaises(IndexError, lambda: Queryable(a)[20])

    def test_getitem_infinite(self):
        b = Queryable(infinite())[5]
        self.assertEqual(b, 5)

    def test_getitem_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b[0])
