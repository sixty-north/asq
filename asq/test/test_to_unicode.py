import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class TestToUnicode(unittest.TestCase):

    def test_to_unicode(self):
        a = "This is a string"
        b = Queryable(a).to_unicode()
        self.assertEqual(a, b)

    def test_to_unicode_from_sequence(self):
        a = ["This ", "is ", "a ", "string!"]
        b = "This is a string!"
        c = Queryable(a).to_unicode()
        self.assertEqual(b, c)

    def test_to_unicode_from_empty_sequence(self):
        a = []
        b = ""
        c = Queryable(a).to_unicode()
        self.assertEqual(b, c)

    def test_to_unicode_empty_with_separator(self):
        a = []
        b = Queryable(a).to_unicode(separator=', ')
        c = ""
        self.assertEqual(b, c)

    def test_to_unicode_one_with_separator(self):
        a = ['string']
        b = Queryable(a).to_unicode(separator=', ')
        c = "string"
        self.assertEqual(b, c)

    def test_to_unicode_many_with_separator(self):
        a = ['this', 'list', 'will', 'be', 'separated', 'by', 'semicolons']
        b = Queryable(a).to_unicode(separator='; ')
        c = "this; list; will; be; separated; by; semicolons"
        self.assertEqual(b, c)

    def test_to_unicode_stringify_separator(self):
        a = ['this', 'list', 'will', 'be', 'separated', 'by', 'fives']
        b = Queryable(a).to_unicode(separator=5)
        c = "this5list5will5be5separated5by5fives"
        self.assertEqual(b, c)

    def test_stringify_items(self):
        a = [1, 5, 9, 34, 12, 3, 67, 1, 0]
        b = Queryable(a).to_unicode(separator=', ')
        c = "1, 5, 9, 34, 12, 3, 67, 1, 0"
        self.assertEqual(b, c)

    def test_to_unicode_closed(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.to_unicode())
