import unittest
from src.asq._portability import has_unicode_type
from src.asq.queryables import Queryable

__author__ = "Sixty North"

if has_unicode_type():

    # This is done to keep PyCharm and various other Python test discovery
    # frameworks happy on Python 3.  They mostly ignore the preceding
    # conditional.

    u = unicode

    class TestUnicode(unittest.TestCase):

        def test_to_unicode(self):
            a = u("This is a string")
            b = unicode(Queryable(a))
            self.assertEqual(a, b)

        def test_to_unicode_from_sequence(self):
            a = [u("This "), u("is "), u("a "), u("string!")]
            b = u("This is a string!")
            c = unicode(Queryable(a))
            self.assertEqual(b, c)

        def test_to_unicode_from_empty_sequence(self):
            a = []
            b = u("")
            c = unicode(Queryable(a))
            self.assertEqual(b, c)

        def test_stringify_items(self):
            a = [1, 5, 9, 34, 12, 3, 67, 1, 0]
            b = unicode(Queryable(a))
            c = u("159341236710")
            self.assertEqual(b, c)

        def test_to_unicode_closed(self):
            a = [u('Aardvark'), u('Balloon'), u('Carrot'), u('Daisy'), u('Ecological')]
            b = Queryable(a)
            b.close()
            self.assertRaises(ValueError, lambda: unicode(b))
