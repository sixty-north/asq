import operator
import unittest
from asq.queryables import Queryable

__author__ = "Sixty North"

class TestPreScan(unittest.TestCase):

    def test_pre_scan_empty_default(self):
        a = []
        b = Queryable(a).pre_scan().to_list()
        c = []
        self.assertEqual(b, c)

    def test_pre_scan_single_default(self):
        a = [47]
        b = Queryable(a).pre_scan().to_list()
        c = [0]
        self.assertEqual(b, c)

    def test_pre_scan_default(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).pre_scan().to_list()
        c = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]
        self.assertEqual(b, c)

    def test_pre_scan_empty_func(self):
        a = []
        b = Queryable(a).pre_scan(operator.mul).to_list()
        c = []
        self.assertEqual(b, c)

    def test_pre_scan_single_func(self):
        a = [47]
        b = Queryable(a).pre_scan(operator.mul, seed=1).to_list()
        c = [1]
        self.assertEqual(b, c)

    def test_pre_scan_func(self):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = Queryable(a).pre_scan(operator.mul, seed=1).to_list()
        c = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        self.assertEqual(b, c)

    def test_pre_scan_func_callable(self):
        self.assertRaises(TypeError, lambda: Queryable([1, 2, 3]).pre_scan("not callable"))

    def test_pre_scan_closed(self):
        b = Queryable([])
        b.close()
        self.assertRaises(ValueError, lambda: b.pre_scan())
  