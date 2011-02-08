import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestEmpty(unittest.TestCase):

    def test_empty_singleton(self):
        self.assertTrue(Queryable.empty() is Queryable.empty())

    def test_empty_count(self):
        self.assertEqual(Queryable.empty().count(), 0)

  