from app.modules.db import DbConnection
from app.modules.Strategy import Strategy
from datetime import date 
from dateutil.relativedelta import relativedelta
from flask_mail import Mail, Message
from app import app
import requests
# daily check will loop through all 
# user strategies in the database and see if we need to check the 
# status of 

class DailyChecker:
	def __init__(self):
		print("Initializing Checker")
		db = DbConnection.getInstance()
		all_poss = db.get_all_user_strategies()
		all_strategies = db.get_strategies()

		today = date.today()
		week_before = today + relativedelta(weeks=-1)
		month_before = today + relativedelta(months=-1)

		need_checked = []
		for user_strat in all_poss:
			if user_strat['interim'] == 'daily':
				need_checked.append(user_strat)
			elif user_strat['interim'] == 'weekly':
				if user_strat['last_check'] == week_before:
					need_checked.append(user_strat)
			elif user_strat['interim'] == 'monthly':
				if user_strat['last_check'] == month_before:
					need_checked.append(user_strat)
		print(len(need_checked))
		self.check_me = need_checked
		self.strategies = [s[0] for s in all_strategies]

	def execute(self):
		strat_map = {}
		for strategy in self.strategies:
			strat_map[strategy] = Strategy(strategy)
			print(strategy)
			print(strat_map[strategy].name)
		for strat in self.check_me:
			print(strat['email'],strat['symbol'],strat['name'])
			notify = strat_map[strat['name']].check_status(strat['symbol'])
			print(notify)
			params = {
				'email':strat['email'],
				'strategy':strat['name'],
				'symbol':strat['symbol'],
				'status':notify
			}
			if notify != 0:
				with app.app_context():
					mail = Mail(app)
					msg = Message('Hello', sender = 'trade.assistant.flask@gmail.com', recipients = [strat['email']])
					msg.body = "Hello Flask message sent from Flask-Mail"
					mail.send(msg)
				return "Sent"
