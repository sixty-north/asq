import unittest
from asq.comparers import insensitive_eq

__author__ = "Robert Smallshire"

class TestComparers(unittest.TestCase):

    def test_case_insensitive_positive(self):
        self.assertTrue(insensitive_eq("abcd", "ABCD"))

    def test_case_insensitive_negative(self):
        self.assertFalse(insensitive_eq("abcd", "wxyz"))

