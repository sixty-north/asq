import sys
import unittest
from src.asq.queryables import Queryable

__author__ = "Sixty North"

if not sys.platform == 'cli':

    class TestAsParallel(unittest.TestCase):

        def test_as_parallel_closed(self):
            b = Queryable([1])
            b.close()
            self.assertRaises(ValueError, lambda: b.as_parallel())