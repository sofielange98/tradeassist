import unittest
import sys
import os
from flask import Flask
import sys

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import app

from app.modules.db import DbConnection

class TradeAssistTest(unittest.TestCase):
    def test_test(self):
    	self.assertTrue(True)

    def test_singleton(self):
    	self.db = DbConnection().getInstance()
    	x = self.db.getInstance()
    	y = self.db.getInstance()
    	self.assertTrue( x is y )

if __name__ == '__main__':
    unittest.main()
