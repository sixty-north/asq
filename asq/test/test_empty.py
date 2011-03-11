import unittest
from asq.queryable import empty

__author__ = 'rjs'

class TestEmpty(unittest.TestCase):

    def test_empty_singleton(self):
        self.assertTrue(empty() is empty())

    def test_empty_count(self):
        self.assertEqual(empty().count(), 0)





  