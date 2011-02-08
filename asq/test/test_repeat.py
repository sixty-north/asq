import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestRepeat(unittest.TestCase):

    def test_repeat(self):
        b = Queryable.repeat('x', 3).to_list()
        self.assertEqual(b, ['x', 'x', 'x'])

    def test_repeat_count_zero(self):
        b = Queryable.repeat('y', 0).to_list()
        self.assertEqual(b, [])

    def test_repeat_negative_count(self):
        self.assertRaises(ValueError, lambda: Queryable.repeat(0, -1))

  