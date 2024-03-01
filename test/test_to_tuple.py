import unittest
from src.asq.queryables import Queryable

class TestToTuple(unittest.TestCase):

    def test_to_tuple(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a).to_tuple()
        c = (27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4)
        self.assertEqual(b, c)

    def test_to_tuple_identity(self):
        a = (27, 74, 18, 48, 57, 97)
        b = Queryable(a).to_tuple()
        self.assertTrue(a is b)

    def test_to_tuple_closed(self):
        a = [27, 74, 18, 48, 57, 97, 76, 20, 91, 8, 80, 59, 20, 32, 58, 12, 74, 78, 4]
        b = Queryable(a)
        b.close()
        self.assertRaises(ValueError, lambda: b.to_tuple())
