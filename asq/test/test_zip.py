import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import TracingGenerator, infinite

__author__ = 'rjs'

class TestZip(unittest.TestCase):

    def test_zip(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        c = Queryable(a).zip(b).to_list()
        self.assertEqual(c, [(1, 4), (2, 5), (3, 6)])

    def test_zip_func(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        c = Queryable(a).zip(b, lambda x, y: int(str(x) + str(y))).to_list()
        self.assertEqual(c, [(14), (25), (36)])

    def test_zip_shorter_longer(self):
        a = [1, 2]
        b = [4, 5, 6]
        c = Queryable(a).zip(b).to_list()
        self.assertEqual(c, [(1, 4), (2, 5)])

    def test_zip_longer_shorter(self):
        a = [1, 2, 3]
        b = [4, 5]
        c = Queryable(a).zip(b).to_list()
        self.assertEqual(c, [(1, 4), (2, 5)])

    def test_zip_empty_longer(self):
        a = []
        b = [4, 5, 6]
        c = Queryable(a).zip(b).to_list()
        self.assertEqual(c, [])

    def test_zip_longer_empty(self):
        a = [1, 2, 3]
        b = []
        c = Queryable(a).zip(b).to_list()
        self.assertEqual(c, [])

    def test_zip_infinite(self):
        c = Queryable(infinite()).zip(infinite()).take(4).to_list()
        self.assertEqual(c, [(0, 0), (1, 1), (2, 2), (3, 3)])

    def test_zip_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = TracingGenerator()
        self.assertEqual(b.trace, [])
        c = Queryable(a).zip(b)
        self.assertEqual(a.trace, [])
        self.assertEqual(b.trace, [])
        d = c.take(4).to_list()
        self.assertEqual(d, [(0, 0), (1, 1), (2, 2), (3, 3)])

    def test_zip_closed(self):
        a = Queryable([1, 2, 3])
        a.close()
        self.assertRaises(ValueError, lambda: a.zip([4, 5, 6]))
        
