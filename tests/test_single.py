import unittest
from asq.queryables import Queryable

__author__ = "Sixty North"

class TestSingle(unittest.TestCase):

    def test_single(self):
        a = [5]
        b = Queryable(a).single()
        self.assertEqual(b, 5)

    def test_single_empty(self):
        a = []
        self.assertRaises(ValueError, lambda: Queryable(a).single())

    def test_single_multiple(self):
        a = [4, 7]
        self.assertRaises(ValueError, lambda: Queryable(a).single())

    def test_single_predicate(self):
        a = ["Aardvark", "Cat", "Dog", "Elephant"]
        b = Queryable(a).single(lambda x: x.startswith('D'))
        self.assertEqual(b, "Dog")

    def test_single_predicate_not_callable(self):
        a = ["Aardvark", "Cat", "Dog", "Elephant"]
        self.assertRaises(TypeError, lambda: Queryable(a).single("not callable"))

    def test_single_predicate_empty(self):
        a = []
        self.assertRaises(ValueError, lambda: Queryable(a).single(lambda x: x.startswith('D')))

    def test_single_predicate_multiple(self):
        a = ["Aardvark", "Cat", "Dog", "Elephant", "Dolphin"]
        self.assertRaises(ValueError, lambda: Queryable(a).single(lambda x: x.startswith('D')))

    def test_single_closed(self):
        a = [5]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.single())

