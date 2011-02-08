import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestReverse(unittest.TestCase):

    # TODO: Text reverse empty

    def test_reverse(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).reverse().to_list()
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)
