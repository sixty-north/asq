import unittest
from src.asq.initiators import empty

__author__ = "Sixty North"

class TestEmpty(unittest.TestCase):

    def test_empty_singleton(self):
        self.assertTrue(empty() is empty())

    def test_empty_count(self):
        self.assertEqual(empty().count(), 0)





