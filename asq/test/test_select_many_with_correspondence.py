import unittest
from asq.queryable import Queryable
from asq.test.test_queryable import infinite, TracingGenerator

class TestSelectManyWithCorrespondence(unittest.TestCase):

    def test_select_many_with_correspondence(self):
        a = ['Alice', 'Bob', 'Chris']
        b = Queryable(a).select_many_with_correspondence(list, lambda x, y: (x, y)).to_list()
        c = [('Alice', 'A'), ('Alice', 'l'), ('Alice', 'i'), ('Alice', 'c'), ('Alice', 'e'), ('Bob', 'B'), ('Bob', 'o'),
             ('Bob', 'b'), ('Chris', 'C'), ('Chris', 'h'), ('Chris', 'r'), ('Chris', 'i'), ('Chris', 's')]
        self.assertEqual(b, c)

    def test_select_many_with_correspondence_projector_not_callable(self):
        a = ['Alice', 'Bob', 'Chris']
        self.assertRaises(TypeError, lambda: Queryable(a).select_many_with_correspondence("not callable", lambda x, y: (x, y)))

    def test_select_many_with_correspondence_selector_not_callable(self):
        a = ['Alice', 'Bob', 'Chris']
        self.assertRaises(TypeError, lambda: Queryable(a).select_many_with_correspondence(list, "not callable"))

    def test_select_many_with_correspondence_infinite(self):
        a = infinite()
        b = Queryable(a).select_many_with_correspondence(lambda x: [x] * x).take(10).to_list()
        c = [(1, 1), (2, 2), (2, 2), (3, 3), (3, 3), (3, 3), (4, 4), (4, 4), (4, 4), (4, 4)]
        self.assertEqual(b, c)

    def test_select_many_with_correspondence_deferred(self):
        a = TracingGenerator()
        self.assertEqual(a.trace, [])
        b = Queryable(a).select_many_with_correspondence(lambda x: [x] * x)
        self.assertEqual(a.trace, [])
        b.take(10).to_list()
        self.assertEqual(a.trace, [0, 1, 2, 3, 4])

    def test_select_many_with_correspondence_closed(self):
        a = ['Alice', 'Bob', 'Chris']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.select_many_with_correspondence(list, lambda x, y: (x, y)))
