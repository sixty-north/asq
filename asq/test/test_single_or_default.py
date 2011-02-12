import unittest
from asq.queryable import Queryable

__author__ = 'rjs'

class TestSingleOrDefault(unittest.TestCase):

    def test_single_or_default(self):
        a = [5]
        b = Queryable(a).single_or_default(7)
        self.assertEqual(b, 5)

    def test_single_or_default_empty(self):
        a = []
        b = Queryable(a).single_or_default(7)
        self.assertEqual(b, 7)

    def test_single_or_default_multiple(self):
        a = [5, 7, 2, 3, 1]
        self.assertRaises(ValueError, lambda: Queryable(a).single_or_default(13))

    def test_single_or_default_predicate_positive(self):
        a = ["Aardvark", "Cat", "Dog", "Elephant"]
        b = Queryable(a).single_or_default('Animal', lambda x: x.startswith('D'))
        self.assertEqual(b, "Dog")

    def test_single_or_default_predicate_negative(self):
        a = ["Aardvark", "Cat", "Elephant"]
        b = Queryable(a).single_or_default('Animal', lambda x: x.startswith('D'))
        self.assertEqual(b, "Animal")

    def test_single_or_default_predicate_empty(self):
        a = []
        b = Queryable(a).single_or_default('foo', lambda x: x.startswith('D'))
        self.assertEqual(b, 'foo')

    def test_single_or_default_predicate_multiple(self):
        a = ["Aardvark", "Cat", "Dog", "Elephant", "Dolphin"]
        self.assertRaises(ValueError, lambda: Queryable(a).single_or_default('Animal', lambda x: x.startswith('D')))

    def test_single_or_default_closed(self):
        a = [5]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.single_or_default(7))
    