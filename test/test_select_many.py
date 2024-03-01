import unittest
from src.asq.queryables import Queryable
from helpers import infinite, TracingGenerator

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

    def test_select_many_projector_not_callable(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        self.assertRaises(TypeError, lambda: Queryable(a).select_many("not callable", lambda y: chr(ord(y)+1)))

    def test_select_many_infinite(self):
        a = infinite()
        b = Queryable(a).select_many(lambda x: [x] * x).take(10).to_list()
        c = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
        self.assertEqual(b, c)

    def test_select_many_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).select_many(lambda x: [x] * x)
        self.assertEqual(a.trace, [])
        b.take(10).to_list()
        self.assertEqual(a.trace, [0, 1, 2, 3, 4])

    def test_select_many_selector_not_callable(self):
        a = ['fox', 'kangaroo', 'bison', 'bear']
        self.assertRaises(TypeError, lambda: Queryable(a).select_many(lambda x : x, "not callable"))

    def test_select_many_closed(self):
        b = Queryable([1, 2, 4, 8])
        b.close()
        self.assertRaises(ValueError, lambda: b.select_many(lambda x: x * 2))