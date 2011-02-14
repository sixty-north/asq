import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestOfType(unittest.TestCase):

    def test_of_type_int(self):
        a = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        b = Queryable(a).of_type(int).to_list()
        c = [2, 3, 6, 8, 9]
        self.assertEqual(b, c)

    def test_of_type_str(self):
        a = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        d = Queryable(a).of_type(str).to_list()
        e = ['one', 'four', 'five', 'seven', 'ten']
        self.assertEqual(d, e)

    def test_of_type_tuple(self):
        a = ['one', 2, 3, 'four', 3.2, 'five', 6, 'seven', 8, 9, 'ten', 9.4]
        d = Queryable(a).of_type((str, int)).to_list()
        e = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        self.assertEqual(d, e)

    def test_of_type_not_type(self):
        a = ['one', 2, 3, 'four', 'five', 6, 'seven', 8, 9, 'ten']
        self.assertRaises(TypeError, lambda: Queryable(a).of_type(7))

    def test_of_type_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.of_type(str))