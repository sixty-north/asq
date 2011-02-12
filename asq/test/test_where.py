import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestWhere(unittest.TestCase):

    def test_where(self):
        a = range(0, 100)
        b = Queryable(a).where(lambda x: x % 3 == 0).to_list()
        c = list(range(0, 100, 3))
        self.assertEqual(b, c)

    def test_where_closed(self):
        a = range(0, 100)
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.where(lambda x: x % 3 == 0))