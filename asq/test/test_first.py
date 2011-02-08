import unittest
from asq.queryable import Queryable
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

    def test_first_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.first())
