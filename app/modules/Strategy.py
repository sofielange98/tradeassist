from app.modules.apikey import API_Interface
import requests
import json
from datetime import date, datetime
import enum 
from app import app 

class Signal(enum.Enum):
	sell = -1
	none = 0 
	buy = 1

class Series(enum.Enum):
	open = 1
	high = 2
	low = 3 
	close = 4
	volume = 5

class Strategy:
#
# check status will return results of calling api for given strategy and return buy/sell/none
#
	def check_status(self, symbol):
		triggered = False
# https://www.alphavantage.co/query?function=MACD&symbol=MSFT&interval=daily&series_type=open&apikey=demo
		with app.app_context():
			params = {
				'apikey' : app.config['ALPHA_API_KEY'],
				'symbol' : symbol,
				'function' : self.api_func,
				'interval' : 'daily',
				'series_type' : 'open'
			}
		if self.api_func == 'BBANDS':
			params['time_period'] = 60
		resp = requests.get(url = self.api_url, params = params)
		print(resp.status_code)
		if resp.status_code == 200: # OK
			s = json.dumps(resp.json())
			y = json.loads(s)
			if 'Note' in y:
				return 'none'

			signal = self.signal_check(y)
			if signal not in [0,1,-1]:
				signal = 0
			return(Signal(signal).name)
		else:
			return 'none'

	def init_dates(self, numbers):
		d = numbers.keys()	
		d = sorted(d, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
		self.curr_date = d[-1]
		self.prev_date = d[-2]
		print(self.curr_date)
		print(self.prev_date)

	def cross_over(self, prev, curr, stat, signal):
		if float(prev[stat]) > float(prev[signal]) and float(curr[stat]) < float(curr[signal]):
			return(-1)
		elif float(prev[stat]) < float(prev[signal]) and float(curr[stat]) > float(curr[signal]):
			return(1)
		else:
			return(0)

	def macd_check(self, api_res):
		#when macd crosses above signal we buy
		numbers = api_res["Technical Analysis: MACD"]
		self.init_dates(numbers)
		today = date.today().isoformat()
		curr = numbers[self.curr_date]
		prev = numbers[self.prev_date]
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "MACD", "MACD_Signal"))

		#when macd crosses below signal we sell
	
	def stochastic_check(self, api_res):
		# when k moves above d, we buy
		numbers = api_res["Technical Analysis: STOCH"]
		self.init_dates(numbers)
		curr = numbers[self.curr_date]
		prev = numbers[self.prev_date]
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "SlowK", "SlowD"))
		# when d moves below k, we buy

	def get_price_value(self, series_type, symbol):
		params = {
			'series_type':series_type,
			'symbol':symbol,
			'function':'TIME_SERIES_DAILY',
			'apikey':app.config['ALPHA_API_KEY']
		}

		resp = requests.get(url = self.api_url, params = params)
		s = json.dumps(resp.json())
		y = json.loads(s)
		time_series = y['Time Series (Daily)']
		prices = {}
		for day in [self.prev_date, self.curr_date]:
			prices[day] = time_series[day]["{}. {}".format(Series[series_type].value, series_type)]
		return prices

	def bollinger_check(self, api_res):
		
		numbers = api_res["Technical Analysis: BBANDS"]
		self.init_dates(numbers)
		curr_price = numbers[self.curr_date]
		prev_price = numbers[self.prev_date]

		vals = self.get_price_value("close", api_res["Meta Data"]["1: Symbol"])
		
		if vals[self.prev_date] > curr_price["Real Lower Band"] and vals[self.curr_date] <= curr_price["Real Lower Band"]:
			return -1
		elif vals[self.prev_date] < curr_price["Real Upper Band"] and vals[self.curr_date] >= curr_price["Real Upper Band"]:
			return 1
		else:
			return 0

	def __init__(self, name):
		self.api_url = 'https://www.alphavantage.co/query?'
		self.name = name
		name_to_func = {
			"MACD":self.macd_check,
			"STOCHASTIC":self.stochastic_check,
			"BOLLINGER":self.bollinger_check
			}
		name_to_api_func = {
			"MACD":'MACD',
			"STOCHASTIC":"STOCH",
			"BOLLINGER":"BBANDS"
			}
		self.api_func = name_to_api_func[name]
		self.signal_check = name_to_func[name]

class Macd(Strategy):
	def signal_check(self, api_res):
		#when macd crosses above signal we buy
		numbers = api_res["Technical Analysis: MACD"]
		today = date.today().isoformat()
		curr = numbers['2019-11-01']
		prev = numbers['2019-10-31']
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "MACD", "MACD_Signal"))	

class Stochastic(Strategy):
	def signal_check(self, api_res):
		# when k moves above d, we buy
		numbers = api_res["Technical Analysis: STOCH"]
		dates = numbers.keys()
		curr = numbers[dates[0]]
		prev = numbers['2019-10-31']
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "SlowK", "SlowD"))

class Bollinger(Strategy):
	def get_price_value(self, series_type, symbol, dates):
		params = {
			'series_type':series_type,
			'symbol':symbol,
			'function':'TIME_SERIES_DAILY',
			'apikey':app.config['ALPHA_API_KEY']
		}

		resp = requests.get(url = self.api_url, params = params)
		s = json.dumps(resp.json())
		y = json.loads(s)
		time_series = y['Time Series (Daily)']
		prices = {}
		for day in [self.prev_date, self.curr_date]:
			prices[day] = time_series[day]["{}. {}".format(Series[series_type].value, series_type)]
		return prices

	def signal_check(self, api_res):
		dates = ['2019-11-01','2019-10-31']
		vals = self.get_price_value("close", api_res["Meta Data"]["1: Symbol"], dates)
		numbers = api_res["Technical Analysis: BBANDS"]
		curr = numbers[dates[0]]
		prev = numbers[dates[1]]
		if vals[dates[1]] > curr["Real Lower Band"] and vals[dates[0]] <= curr["Real Lower Band"]:
			return -1
		elif vals[dates[1]] < curr["Real Upper Band"] and vals[dates[0]] >= curr["Real Upper Band"]:
			return 1
		else:
			return 0


