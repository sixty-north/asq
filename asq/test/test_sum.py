import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestSum(unittest.TestCase):

    def test_sum(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a).sum()
        self.assertEqual(b, 26)

    def test_sum_selector(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        b = Queryable(a).sum(abs)
        self.assertEqual(b, 53)

    def test_sum_selector_not_callable(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -13, 7]
        self.assertRaises(TypeError, lambda: Queryable(a).sum("not callable"))
            
    def test_sum_empty(self):
        b = Queryable([]).sum()
        self.assertEqual(b, 0)

    def test_sum_closed(self):
        a = [5, 7, -3, 2, 1, 9, 3, 2, 1, -8, 7]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.sum())
    
