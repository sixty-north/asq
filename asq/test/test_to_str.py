import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

#class TestToStr(unittest.TestCase):

# TODO: Write tests for str

#    def test_to_set(self):
#        a = set([1, 2, 4, 8, 16, 32])
#        b = Queryable(a).to_set()
#        c = set([1, 2, 3, 8, 16, 32])
#        self.assertEqual(b, c)
#
#    def test_to_set(self):
#        a = [1, 2, 4, 8, 16, 32]
#        b = Queryable(a).to_set()
#        c = set([1, 2, 4, 8, 16, 32])
#        self.assertEqual(b, c)
#
#    def test_to_set_closed(self):
#        a = [1, 2, 4, 8, 16, 32]
#        b = Queryable(a)
#        b.close()
#        self.assertRaises(ValueError, lambda: b.to_set())
#
#    def test_to_set_duplicates(self):
#        a = [1, 2, 4, 8, 8, 16, 32]
#        b = Queryable(a)
#        self.assertRaises(ValueError, lambda: b.to_set())
