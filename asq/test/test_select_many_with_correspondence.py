import unittest
from asq.queryable import Queryable

class TestSelectManyWithCorrespondence(unittest.TestCase):

    def test_select_many_with_correspondence(self):
        a = ['Alice', 'Bob', 'Chris']
        b = Queryable(a).select_many_with_correspondence(list, lambda x, y: (x, y)).to_list()
        c = [('Alice', 'A'), ('Alice', 'l'), ('Alice', 'i'), ('Alice', 'c'), ('Alice', 'e'), ('Bob', 'B'), ('Bob', 'o'),
             ('Bob', 'b'), ('Chris', 'C'), ('Chris', 'h'), ('Chris', 'r'), ('Chris', 'i'), ('Chris', 's')]
        self.assertEqual(b, c)

    def test_select_many_with_correspondence_closed(self):
        a = ['Alice', 'Bob', 'Chris']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.select_many_with_correspondence(list, lambda x, y: (x, y)))
