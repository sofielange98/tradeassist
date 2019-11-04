import unittest
import sys
import os
from flask import Flask
from app.db import DbConnection
# TEST_DIR = os.path.dirname(os.path.abspath(__file__))

class TradeAssistTest(unittest.TestCase):
    def test_test(self):
    	self.assertTrue(True)

    def test_singleton(self):
    	self.db = DbConnection()
    	x = self.db.getInstance()
    	y = self.db.getInstance()
    	self.assertTrue( x is y )


if __name__ == '__main__':
    unittest.main()
