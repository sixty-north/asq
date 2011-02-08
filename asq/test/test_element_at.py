import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import infinite

__author__ = 'rjs'

class TestElementAt(unittest.TestCase):

    def test_element_at(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        b = Queryable(a).element_at(3)
        self.assertEqual(b, 8)

    def test_element_at_out_of_range_infinite(self):
        self.assertRaises(ValueError, lambda: Queryable(infinite()).element_at(-1))

    def test_element_at_out_of_range(self):
        a = [1, 2, 4, 8, 16, 32, 64, 128]
        self.assertRaises(ValueError, lambda: Queryable(a).element_at(20))

    def test_element_at_infinite(self):
        b = Queryable(infinite()).element_at(5)
        self.assertEqual(b, 5)
