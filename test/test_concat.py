import unittest
from asq.queryables import Queryable
from helpers import TracingGenerator, infinite

__author__ = "Sixty North"

class TestConcat(unittest.TestCase):

    def test_concat(self):
        a = [1, 2, 3]
        b = Queryable(a).concat([4, 5, 6]).to_list()
        c = [1, 2, 3, 4, 5, 6]
        self.assertEqual(b, c)

    def test_concat_infinite(self):
        b = Queryable(infinite()).concat(infinite()).take(3).to_list()
        c = [0, 1, 2]
        self.assertEqual(b, c)

    def test_concat_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = TracingGenerator()
        self.assertEqual(b.trace, [])
        c = Queryable(a).concat(b).take().to_list()
        self.assertEqual(a.trace, [0])
        self.assertEqual(b.trace, [])

    def test_concat_non_iterable(self):
        a = [1, 2, 3, 4, 5]
        self.assertRaises(TypeError, lambda: Queryable(a).concat(7))

    def test_concat_closed(self):
        b = Queryable([1])
        b.close()
        self.assertRaises(ValueError, lambda: b.concat([2]))
