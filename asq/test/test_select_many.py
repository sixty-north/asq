import unittest
from asq.queryable import Queryable

class TestSelectMany(unittest.TestCase):

    def test_select_many_projector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        b = Queryable(a).select_many(lambda x : x).to_list()
        c = ['f', 'o', 'x', 'k', 'a', 'n', 'g', 'a', 'r', 'o', 'o', 'b', 'i', 's', 'o', 'n', 'b', 'e', 'a', 'r']
        self.assertEqual(b, c)

    def test_select_many_projector_selector_finite(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        b = Queryable(a).select_many(lambda x : x, lambda y: chr(ord(y)+1)).to_list()
        c = ['g', 'p', 'y', 'l', 'b', 'o', 'h', 'b', 's', 'p', 'p', 'c', 'j', 't', 'p', 'o', 'c', 'f', 'b', 's']
        self.assertEqual(b, c)
