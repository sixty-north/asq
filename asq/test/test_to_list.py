import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestToList(unittest.TestCase):

    def test_to_list(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).to_list()
        self.assertEqual(a, b)

    def test_to_list_identity(self):
        a = [27, 74, 18, 48, 57, 97]
        b = Queryable(a).to_list()
        self.assertTrue(a is b)
        