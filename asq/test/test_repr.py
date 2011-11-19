import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class TestRepr(unittest.TestCase):

    def test_repr(self):
        a = "This is a string"
        b = "Queryable('This is a string')"
        c = repr(Queryable(a))
        self.assertEqual(b, c)

    def test_repr_from_sequence(self):
        a = ["This ", "is ", "a ", "string!"]
        b = "Queryable(['This ', 'is ', 'a ', 'string!'])"
        c = repr(Queryable(a))
        self.assertEqual(b, c)

    def test_repr_from_empty_sequence(self):
        a = []
        b = "Queryable([])"
        c = repr(Queryable(a))
        self.assertEqual(b, c)

    def test_repr_closed(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a)
        b.close()
        c = repr(b)
        d = "Queryable(None)"
        self.assertEqual(c, d)

    def test_repr_idempotency(self):
        a = (x for x in range(1, 10))
        b = Queryable(a)
        c = repr(b)
        d = repr(b)
        self.assertEqual(c, d)

    def test_repr_non_consumption(self):
        a = (x for x in range(1, 10))
        b = Queryable(a)
        c = repr(b)
        d = b.to_list()
        e = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(d, e)

    def test_repr_ordered_non_consumption(self):
        a = [x for x in range(10, 1, -1)]
        b = Queryable(a).order_by()
        c = repr(b)
        d = b.to_list()
        e = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(d, e)

        
