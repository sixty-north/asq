"""
test_queryable.py Unit tests for asq.queryable.Queryable
"""
import unittest

from asq.queryables import Queryable


class TestQueryable(unittest.TestCase):

    def test_non_iterable(self):
        self.assertRaises(TypeError, lambda: Queryable(5))
