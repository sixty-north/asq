import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestOrderBy(unittest.TestCase):

    def test_order_by(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).order_by().to_list()
        c = [4, 8, 12, 18, 20, 20, 27, 32, 48, 57, 58, 59, 74, 74, 76, 78, 80, 91, 97]
        self.assertEqual(b, c)

    def test_order_by2(self):
        a = [1, 9, 7, 2, 5, 4, 6, 3, 8, 10]
        b = Queryable(a).order_by().to_list()
        c = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(b, c)

    def test_order_by_key(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a).order_by(len).to_list()
        c = ['by', 'Sort', 'words', 'length']
        self.assertEqual(b, c)

    def test_order_by_not_callable(self):
        a = ['Sort', 'words', 'by', 'length']
        self.assertRaises(TypeError, lambda: Queryable(a).order_by("not callable"))

    def test_order_by_closed(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.order_by(len))

    def test_then_by(self):
        a = ['sort', 'these', 'words', 'by', 'length', 'and', 'then', 'lexicographically']
        b = Queryable(a).order_by(len).then_by().to_list()
        c = ['by', 'and', 'sort', 'then', 'these', 'words', 'length', 'lexicographically']
        self.assertEqual(b, c)

    def test_then_by_key(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2]).then_by(lambda y: y[1]).to_list()
        c = ['second', 'then', 'third', 'using', 'sort', 'letter']
        self.assertEqual(b, c)

    def test_then_by_not_callable(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2])
        self.assertRaises(TypeError, lambda: b.then_by("not callable"))

    def test_then_by_closed(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2])
        b.close()
        self.assertRaises(ValueError, lambda: b.then_by(lambda x: x[1]))

    def test_order_by_descending(self):
        a = [1, 9, 7, 2, 5, 4, 6, 3, 8, 10]
        b = Queryable(a).order_by_descending().to_list()
        c = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.assertEqual(b, c)

    def test_order_by_descending_key(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a).order_by_descending(len).to_list()
        c = ['length', 'words', 'Sort', 'by']
        self.assertEqual(b, c)

    def test_order_by_descending_not_callable(self):
        a = ['Sort', 'words', 'by', 'length']
        self.assertRaises(TypeError, lambda: Queryable(a).order_by_descending("not callable"))

    def test_order_by_descending_closed(self):
        a = ['Sort', 'words', 'by', 'length']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.order_by_descending(len))

    def test_then_by_descending(self):
        a = ['sort', 'these', 'words', 'by', 'length', 'and', 'then', 'lexicographically']
        b = Queryable(a).order_by(len).then_by_descending().to_list()
        c = ['by', 'and', 'then', 'sort', 'words', 'these', 'length', 'lexicographically']
        self.assertEqual(b, c)

    def test_then_by_descending_key(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2]).then_by_descending(lambda y: y[1]).to_list()
        c = ['second', 'then', 'using', 'third', 'sort', 'letter']
        self.assertEqual(b, c)

    def test_then_by_descending_not_callable(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2])
        self.assertRaises(TypeError, lambda: b.then_by_descending("not callable"))

    def test_then_by_descending_closed(self):
        a = ['sort', 'using', 'third', 'letter', 'then', 'second']
        b = Queryable(a).order_by(lambda x: x[2])
        b.close()
        self.assertRaises(ValueError, lambda: b.then_by_descending(lambda x: x[1]))
