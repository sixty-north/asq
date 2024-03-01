import unittest
import pickle

from asq.record import Record, new

__author__ = "Sixty North"

class TestRecord(unittest.TestCase):

    def test_create(self):
        r = Record(x=10, y=20, z=30)
        self.assertEqual(r.x, 10)
        self.assertEqual(r.y, 20)
        self.assertEqual(r.z, 30)

    def test_create_positional_error(self):
        self.assertRaises(TypeError, lambda: Record(10, 20, 30))

    def test_create_empty(self):
        r = Record()

    def test_record_equality_positive(self):
        a = Record(x=10, y=20, z=30)
        b = Record(x=10, y=20, z=30)
        self.assertTrue(a == b)

    def test_record_equality_negative(self):
        a = Record(x=10, y=20, z=30)
        b = Record(x=10, y=40, z=30)
        self.assertFalse(a == b)

    def test_record_inequality_positive(self):
        a = Record(x=10, y=20, z=30)
        b = Record(x=10, y=40, z=30)
        self.assertTrue(a != b)

    def test_record_inequality_negative(self):
        a = Record(x=10, y=20, z=30)
        b = Record(x=10, y=20, z=30)
        self.assertFalse(a != b)

    def test_record_pickle_roundtrip(self):
        a = Record(x=20, y=80, z=50)
        s = pickle.dumps(a)
        b = pickle.loads(s)
        self.assertEqual(a, b)

    def test_record_str(self):
        a = Record(x=20, y=30, z=40)
        s= str(a)
        self.assertTrue("x=20" in s)
        self.assertTrue("y=30" in s)
        self.assertTrue("z=40" in s)

    def test_record_repr(self):
        a = Record(x=20, y=30, z=40)
        s= repr(a)
        self.assertTrue(s.startswith("Record("))
        self.assertTrue("x=20" in s)
        self.assertTrue("y=30" in s)
        self.assertTrue("z=40" in s)
        self.assertTrue(s.endswith(")"))

    def test_new_create(self):
        r = new(x=10, y=20, z=30)
        self.assertEqual(r.x, 10)
        self.assertEqual(r.y, 20)
        self.assertEqual(r.z, 30)

    def test_new_create_positional_error(self):
        self.assertRaises(TypeError, lambda: new(10, 20, 30))

    def test_new_create_empty(self):
        r = new()








