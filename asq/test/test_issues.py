import unittest
from asq.initiators import query


__author__ = 'rjs'

class TestIssue4(unittest.TestCase):

    def test_order_by_count(self):
        x = query([1,2,3]).order_by()
        c = x.count()
        self.assertEqual(c, 3)

    def test_order_by_first(self):
        x = query([1,2,3]).order_by()
        first = x.first()
        self.assertEqual(first, 1)

    def test_order_by_count_first(self):
        x = query([1,2,3]).order_by()
        c = x.count()
        self.assertEqual(c, 3)
        first = x.first()
        self.assertEqual(first, 1)



