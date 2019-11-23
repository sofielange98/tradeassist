from app.modules.db import DbConnection
from app.modules.Strategy import Strategy
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask_mail import Mail, Message
from flask import current_app, g
from app import app 

import requests
import time
# daily check will loop through all 
# user strategies in the database and see if we need to check the 
# status of 

class DailyChecker:
	def __init__(self):
		print("Initializing Checker")
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

	def create_email(self, params):
		notification = '''
		The {} indicator has triggered a {} signal for the symbol {}.

		Happy Trading!
		'''.format(params['strategy'], params['status'], params['symbol'])

		return notification

	def execute(self):
		strat_map = {}
		for strategy in self.strategies:
			strat_map[strategy] = Strategy(strategy)
			print(strat_map[strategy].name)
		for strat in self.check_me:
			print(strat['email'],strat['symbol'],strat['name'])
			notify = strat_map[strat['name']].check_status(strat['symbol'])
			time.sleep(10)
			print(notify)
			params = {
				'email':strat['email'],
				'strategy':strat['name'],
				'symbol':strat['symbol'],
				'status':notify
			}
			if notify != 0:
				with app.app_context():
					mail = Mail(current_app)
					msg = Message('Time to Trade', sender = 'trade.assistant.flask@gmail.com', recipients = [strat['email']])
					msg.body = self.create_email(params)
					mail.send(msg)
					return "Sent"
