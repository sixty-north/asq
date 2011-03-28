import unittest
from asq.initiators import asq

__author__ = 'rjs'

class TestAsq(unittest.TestCase):

    def test_asq_iterable(self):
        a = [5, 4, 3, 2, 1]
        b = asq(a)

    def test_asq_non_iterable(self):
        self.assertRaises(TypeError, lambda: asq(5))



  