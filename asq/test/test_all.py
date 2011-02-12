import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestAll(unittest.TestCase):

    def test_all_positive(self):
        a = [True, True, True, True]
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_negative(self):
        a = [True, True, True, False]
        b = Queryable(a).all()
        self.assertFalse(b)

    def test_all_empty(self):
        a = []
        b = Queryable(a).all()
        self.assertTrue(b)

    def test_all_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.all())