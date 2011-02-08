import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestOfType(unittest.TestCase):

    def test_of_type(self):
        a = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        b = Queryable(a).of_type(int).to_list()
        c = [2, 3, 6, 8, 9]
        self.assertEqual(b, c)
        d = Queryable(a).of_type(str).to_list()
        e = ['one', 'four', 'five', 'seven', 'ten']
        self.assertEqual(d, e)

