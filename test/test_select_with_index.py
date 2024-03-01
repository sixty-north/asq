import unittest
from src.asq.queryables import Queryable
from helpers import infinite, TracingGenerator


class TestSelectWithIndex(unittest.TestCase):

    def test_select_with_index(self):
        a = [27, 74, 18, 48, 57, 97]
        b = Queryable(a).select_with_index().to_list()
        c = [(0, 27), (1, 74), (2, 18), (3, 48), (4, 57), (5, 97)]
        self.assertEqual(b, c)

    def test_select_with_index_finite(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).select_with_index(lambda x, y: x*y).to_list()
        c = [0, 74, 36, 144, 228, 485, 456, 140, 728, 72, 800, 649, 240, 416, 812, 180, 1184, 1326, 72]
        self.assertEqual(b, c)

    def test_select_with_index_infinite(self):
        a = infinite()
        b = Queryable(a).select_with_index(lambda x, y: x*y).take(4).to_list()
        c = [0, 1, 4, 9]
        self.assertEqual(b, c)

    def test_select_with_index_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).select_with_index()
        self.assertEqual(a.trace, [])
        b.take(3).to_list()
        self.assertEqual(a.trace, [0, 1, 2])

    def test_select_with_index_not_callable(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        self.assertRaises(TypeError, lambda: Queryable(a).select_with_index("not callable"))

    def test_select_with_index_closed(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.select_with_index(lambda x, y: x*y))

