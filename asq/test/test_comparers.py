import unittest
from asq.comparers import insensitive_eq

__author__ = 'rjs'

class TestComparers(unittest.TestCase):

    def case_insensitive_positive(self):
        self.assertTrue(insensitive_eq("abcd", "ABCD"))

    def case_insensitive_negative(self):
        self.assertFalse(insenstive_eq("abcd", "wxyz"))

