import unittest
import sys
import os
from flask import Flask
from app.db import DbConnection
# TEST_DIR = os.path.dirname(os.path.abspath(__file__))

class TradeAssistTest(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_mapping(
          SECRET_KEY='test_key',
          DATABASE=os.path.join(app.instance_path, 'tradeassist.sqlite'),
          )
        
        self.db = DbConnection().getInstance()


if __name__ == '__main__':
    unittest.main()