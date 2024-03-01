import unittest
from asq.queryables import Queryable
from asq.record import new
from helpers import infinite, TracingGenerator

__author__ = "Sixty North"

class TestSelect(unittest.TestCase):

    def test_select(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).select(lambda x: x*2).to_list()
        c = [54, 148, 36, 96, 114, 194, 152, 40, 182, 16, 160, 118, 40, 64, 116, 24, 148, 156, 8]
        self.assertEqual(b, c)

    def test_select_attribute(self):
        a = [new(x=5, y=3, z=10),
             new(x=1, y=7, z=13),
             new(x=9, y=3, z=10),
             new(x=8, y=4, z=12)]
        b = Queryable(a).select('y').to_list()
        c = [3, 7, 3, 4]
        self.assertEqual(b, c)

    def test_select_empty(self):
        a = []
        b = Queryable(a).select(lambda x: x*2).to_list()
        self.assertEqual(a, b)

    def test_select_infinite(self):
        a = infinite()
        b = Queryable(a).select(lambda x: x*2).take(3).to_list()
        c = [0, 2, 4]
        self.assertEqual(b, c)

    def test_select_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).select(lambda x: x*2)
        self.assertEqual(a.trace, [])
        c = b.take(3).to_list()
        self.assertEqual(a.trace, [0, 1, 2])

    def test_select_not_callable(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        self.assertRaises(TypeError, lambda: Queryable(a).select(37))

    def test_select_closed(self):
        b = Queryable([1, 2, 4, 8])
        b.close()
        self.assertRaises(ValueError, lambda: b.select(lambda x: x * 2))