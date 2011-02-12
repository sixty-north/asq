import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestRange(unittest.TestCase):

    def test_range(self):
        b = Queryable.range(54, 7).to_list()
        self.assertEqual(b, [54, 55, 56, 57, 58, 59, 60])

    def test_range(self):
        b = Queryable.range(-3, 6).to_list()
        self.assertEqual(b, [-3, -2, -1, 0, 1, 2])

    def test_range_count_zero(self):
        b = Queryable.range(7, 0).to_list()
        self.assertEqual(b, [])

    def test_range_negative_count(self):
        self.assertRaises(ValueError, lambda: Queryable.range(0, -1))

    def test_range_instance(self):
        Queryable([1, 2, 3]).range(3, 5)
