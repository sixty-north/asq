import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import infinite

__author__ = 'rjs'

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

    def test_first_or_default_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.first_or_default(37))
