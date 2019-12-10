from app.modules.db import DbConnection
from app.modules.Strategy import Strategy
from app.modules.Mailer import Mailer
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask_mail import Mail, Message
from flask import current_app, g
import enum 
from app import app 

import requests
import time

# daily check will loop through all 
# user strategies in the database and see if we need to check the 
# status of 

class DailyChecker:
	def __init__(self):
		print("Initializing Checker")
		if self.is_weekday():
			db = DbConnection.getInstance()
			all_poss = db.get_all_user_strategies()
			self.strategies = db.get_strategies()

			today = datetime.combine(date.today(), datetime.min.time())
			week_before = datetime.combine(date.today() + relativedelta(weeks=-1), datetime.min.time())
			month_before = datetime.combine(date.today() + relativedelta(months=-1), datetime.min.time())

			need_checked = []
			for user_strat in all_poss:
				if user_strat['interim'] == 'daily':
					need_checked.append(user_strat)
				elif user_strat['interim'] == 'weekly':
					if user_strat['last_check'] >= week_before:
						need_checked.append(user_strat)
				elif user_strat['interim'] == 'monthly':
					if user_strat['last_check'] >= month_before:
						need_checked.append(user_strat)
			print("Num checks needed ", len(need_checked))
			self.check_me = need_checked
		else:
			print('Weekend! No trading today!')
			self.strategies = []
			self.check_me = []

	def is_weekday(self):
		day = datetime.today().weekday()
		print(day)
		if day in range(5): # 0,1,2,3,4 correspond to Mon-Fri
			return True
		else:
			return False


	def execute(self):
		strat_map = {}
		for strategy in self.strategies:
			strat_map[strategy] = Strategy(strategy)
			print(strat_map[strategy].name)
		if len(self.check_me) != 0:
			mailer = Mailer()
		for strat in self.check_me:
			print(strat['email'],strat['symbol'],strat['name'])
			notify = strat_map[strat['name']].check_status(strat['symbol'])
			time.sleep(60)
			print(notify)
			params = {
				'email':strat['email'],
				'strategy':strat['name'],
				'symbol':strat['symbol'],
				'status':notify
			}
			if notify != 0:
				mailer.notify(params)
