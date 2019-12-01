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
from app.modules.User import User 

class TradeAssistTest(unittest.TestCase):
	def test_test(self):
		self.assertTrue(True)

	def test_singleton(self):
		self.db = DbConnection.getInstance()
		x = self.db.getInstance()
		y = self.db.getInstance()
		self.assertTrue( x is y )

	def test_add_user(self):
		# user.email, user.username, user.password
		test_user = {
			'username': 'unit test user',
			'email': 'unit@test.com',
			'password':'password'
		}
		test_user = User(test_user)
		self.db = DbConnection.getInstance()
		uid = self.db.insert_new_user(test_user)
		user_db = self.db.get_user_by_id(uid)
		self.assertTrue(user_db is not None)
		self.db.delete_user(test_user)

	
	def test_delete_user(self):
		test_user = {
			'username': 'unit test user',
			'email': 'unit@test.com',
			'password':'password'
		}
		test_user = User(test_user)
		self.db = DbConnection.getInstance()
		self.db.delete_user(test_user)
		print(self.db.check_existing_user(test_user))
		user = self.db.get_user_by_email(test_user.email)
		print(type(user))
		print(user)
		self.assertTrue(user is None)

if __name__ == '__main__':
	unittest.main()