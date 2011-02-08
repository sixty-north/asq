import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestLast(unittest.TestCase):

    def test_last(self):
        a = [42, 45, 23, 12]
        b = Queryable(a).last()
        self.assertEqual(b, 12)

    def test_last_empty(self):
        self.assertRaises(ValueError, lambda: Queryable([]).last())

    def test_last_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.last())

  