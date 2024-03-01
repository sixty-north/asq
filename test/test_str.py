import unittest
from src.asq.queryables import Queryable

__author__ = "Sixty North"

class TestStr(unittest.TestCase):

    def test_to_str(self):
        a = "This is a string"
        b = str(Queryable(a))
        self.assertEqual(a, b)

    def test_to_str_from_sequence(self):
        a = ["This ", "is ", "a ", "string!"]
        b = "This is a string!"
        c = str(Queryable(a))
        self.assertEqual(b, c)

    def test_to_str_from_empty_sequence(self):
        a = []
        b = ""
        c = str(Queryable(a))
        self.assertEqual(b, c)

    def test_stringify_items(self):
        a = [1, 5, 9, 34, 12, 3, 67, 1, 0]
        b = str(Queryable(a))
        c = "159341236710"
        self.assertEqual(b, c)

    def test_to_str_closed(self):
        a = ['Aardvark', 'Balloon', 'Carrot', 'Daisy', 'Ecological']
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: str(b))
