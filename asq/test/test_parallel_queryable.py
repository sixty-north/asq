import sys
import unittest
from asq.queryables import Queryable, identity
from asq.test.test_queryable import times, inc_chr, times_two

if not sys.platform == 'cli':


    class TestParallelQueryable(unittest.TestCase):

        def test_parallel_select(self):
            a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
            with Queryable(a) as q:
                b = q.as_parallel().select(times_two).to_list()
            c = [54, 148, 36, 96, 114, 194, 152, 40, 182, 16, 160, 118, 40, 64, 116, 24, 148, 156, 8]
            self.assertEqual(len(b), len(c))
            self.assertEqual(set(b), set(c))

        def test_parallel_select_with_index_finite(self):
            a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
            with Queryable(a) as q:
                b = q.as_parallel().select_with_index(times).to_list()
            c = [0, 74, 36, 144, 228, 485, 456, 140, 728, 72, 800, 649, 240, 416, 812, 180, 1184, 1326, 72]
            self.assertEqual(len(b), len(c))
            self.assertEqual(set(b), set(c))

        def test_parallel_select_many_projector_finite(self):
            a = ['fox', 'kangaroo', 'bison', 'bear']
            with Queryable(a) as q:
                b = q.as_parallel().select_many(identity).to_list()
            c = ['f', 'o', 'x', 'k', 'a', 'n', 'g', 'a', 'r', 'o', 'o', 'b', 'i', 's', 'o', 'n', 'b', 'e', 'a', 'r']
            self.assertEqual(sorted(b), sorted(c))

        def test_parallel_select_many_projector_selector_finite(self):
            a = ['fox', 'kangaroo', 'bison', 'bear']
            with Queryable(a) as q:
                b = q.as_parallel().select_many(identity, inc_chr).to_list()
            c = ['g', 'p', 'y', 'l', 'b', 'o', 'h', 'b', 's', 'p', 'p', 'c', 'j', 't', 'p', 'o', 'c', 'f', 'b', 's']
            self.assertEqual(len(b), len(c))
            self.assertEqual(set(b), set(c))

        def test_parallel_order_by(self):
            a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
            with Queryable(a) as q:
                b = q.as_parallel().order_by().to_list()
            c = [4, 8, 12, 18, 20, 20, 27, 32, 48, 57, 58, 59, 74, 74, 76, 78, 80, 91, 97]
            self.assertEqual(b, c)

        #def test_parallel_order_by(self):
        #    with Queryable(randgen()) as q:
        #        a = q.as_parallel().take(1000000).order_by().to_list


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParallelQueryable)
    unittest.TextTestRunner(verbosity=2).run(suite)
