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

    def test_last_or_default_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.last_or_default(37))
