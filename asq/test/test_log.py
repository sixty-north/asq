import unittest
from asq.queryables import Queryable

__author__ = 'rjs'

class Logger(object):

    def __init__(self):
        self.log = []

    def debug(self, message):
        self.log.append(message)

class TestLog(unittest.TestCase):

    def test_log_default(self):
        a = [1, 6, 4, 3, 9, 2]
        b = Queryable(a).log().to_list()
        self.assertEqual(a, b)

    def test_log_disable(self):
        a = [1, 6, 4, 3, 9, 2]
        b = Queryable(a).log(logger=None).to_list()
        self.assertEqual(a, b)

    def test_log_enable_deferred(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, eager=False).take(3).to_list()
        self.assertEqual(len(logger.log), 4)
        self.assertTrue(logger.log[0].find('BEGIN') != -1)
        self.assertTrue(logger.log[0].find('DEFERRED') != -1)
        self.assertTrue(logger.log[1].find('yields 1') != -1)
        self.assertTrue(logger.log[2].find('yields 6') != -1)
        self.assertTrue(logger.log[3].find('yields 4') != -1)

    def test_log_enable_eager(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, eager=True).to_list()
        self.assertEqual(len(logger.log), 8)
        self.assertTrue(logger.log[0].find('BEGIN') != -1)
        self.assertTrue(logger.log[0].find('EAGER') != -1)
        self.assertTrue(logger.log[1].find('= 1') != -1)
        self.assertTrue(logger.log[2].find('= 6') != -1)
        self.assertTrue(logger.log[3].find('= 4') != -1)
        self.assertTrue(logger.log[4].find('= 3') != -1)
        self.assertTrue(logger.log[5].find('= 9') != -1)
        self.assertTrue(logger.log[6].find('= 2') != -1)
        self.assertTrue(logger.log[7].find('END') != -1)

    def test_log_label_deferred(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="Test1", eager=False).take(3).to_list()
        for line in logger.log:
            self.assertTrue(line.startswith("Test1"))

    def test_log_label_eager(self):
        a = [1, 6, 4, 3, 9, 2]
        logger = Logger()
        b = Queryable(a).log(logger, label="Test2", eager=True).to_list()
        for line in logger.log:
            self.assertTrue(line.startswith("Test2"))
