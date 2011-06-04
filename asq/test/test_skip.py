import unittest
from asq.queryables import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

__author__ = 'rjs'

class TestSkip(unittest.TestCase):
    
    def test_skip_negative(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip(-1).to_list()
        c = ['a', 'b', 'c']
        self.assertEqual(b, c)

    def test_skip_zero(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip(0).to_list()
        c = ['a', 'b', 'c']
        self.assertEqual(b, c)

    def test_skip_one(self):
        a = ['a', 'b', 'c']
        b = Queryable(a).skip().to_list()
        c = ['b', 'c']
        self.assertEqual(b, c)

    def test_skip_five(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).skip(5).to_list()
        c = ['f', 'g']
        self.assertEqual(b, c)

    def test_skip_too_many(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        b = Queryable(a).skip(10).to_list()
        c = []
        self.assertEqual(b, c)

    def test_skip_from_infinite(self):
        b = Queryable(infinite()).skip(5).take(3).to_list()
        c = [5, 6, 7]
        self.assertEqual(b, c)

    def test_skip_getitem_but_no_len(self):
        class Seq(object):
            def __init__(self, data):
                self.data = data

            def __getitem__(self, index):
                return self.data[index]

        seq = Seq([5, 6, 1, 5, 9])
        b = Queryable(seq).skip(2).to_list()
        c = [1, 5, 9]
        self.assertEqual(b, c)

    def test_skip_is_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).skip(3)
        self.assertEqual(a.trace, [])
        c = b.take().to_list()
        self.assertEqual(a.trace, [0, 1, 2, 3])

    def test_skip_closed(self):
        a = ['a', 'b', 'c']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.skip(1))
        
        
  