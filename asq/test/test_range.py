import unittest
from asq.initiators import integers

__author__ = "Robert Smallshire"

class TestRange(unittest.TestCase):

    def test_range(self):
        b = integers(54, 7).to_list()
        self.assertEqual(b, [54, 55, 56, 57, 58, 59, 60])

    def test_range(self):
        b = integers(-3, 6).to_list()
        self.assertEqual(b, [-3, -2, -1, 0, 1, 2])

    def test_range_count_zero(self):
        b = integers(7, 0).to_list()
        self.assertEqual(b, [])

    def test_range_negative_count(self):
        self.assertRaises(ValueError, lambda: integers(0, -1))

