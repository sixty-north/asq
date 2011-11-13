import operator
import unittest
from asq.queryables import Queryable

__author__ = "Robert Smallshire"

class TestScan(unittest.TestCase):

    def test_scan_empty_default(self):
        a = []
        b = Queryable(a).scan().to_list()
        c = []
        self.assertEqual(b, c)

    def test_scan_single_default(self):
        a = [47]
        b = Queryable(a).scan().to_list()
        c = [47]
        self.assertEqual(b, c)

    def test_scan_default(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).scan().to_list()
        c = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
        self.assertEqual(b, c)

    def test_scan_empty_func(self):
        a = []
        b = Queryable(a).scan(operator.mul).to_list()
        c = []
        self.assertEqual(b, c)

    def test_scan_single_func(self):
        a = [47]
        b = Queryable(a).scan(operator.mul).to_list()
        c = [47]
        self.assertEqual(b, c)

    def test_scan_func(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).scan(operator.mul).to_list()
        c = [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
        self.assertEqual(b, c)

    def test_scan_func_callable(self):
        self.assertRaises(TypeError, lambda: Queryable([1, 2, 3]).scan("not callable"))

    def test_scan_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.scan())
  