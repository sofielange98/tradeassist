from apikey import API_Interface
import requests
import json
from datetime import date 
import enum 

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
	def check_status(self, params):
		triggered = False
# https://www.alphavantage.co/query?function=MACD&symbol=MSFT&interval=daily&series_type=open&apikey=demo
		API = API_Interface.getInstance()
		params['apikey'] = API.key
		resp = requests.get(url = self.api_url, params = params)
		s = json.dumps(resp.json())
		y = json.loads(s)
		signal = self.signal_check(y)
		print(Signal(signal).name)
		return(y)

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
		today = date.today().isoformat()
		curr = numbers['2019-11-01']
		prev = numbers['2019-10-31']
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "MACD", "MACD_Signal"))

		#when macd crosses below signal we sell
	
	def stochastic_check(self, api_res):
		# when k moves above d, we buy
		numbers = api_res["Technical Analysis: STOCH"]
		curr = numbers['2019-11-01']
		prev = numbers['2019-10-31']
		print(curr)
		print(prev)
		return(self.cross_over(prev,curr, "SlowK", "SlowD"))
		# when d moves below k, we buy

	def get_price_value(self, series_type, symbol, dates):
		params = {
			'series_type':series_type,
			'symbol':symbol,
			'function':'TIME_SERIES_DAILY'
		}
		API = API_Interface.getInstance()
		params['apikey'] = API.key

		resp = requests.get(url = self.api_url, params = params)
		s = json.dumps(resp.json())
		y = json.loads(s)
		time_series = y['Time Series (Daily)']
		prices = {}
		for day in dates:
			prices[day] = time_series[day]["{}. {}".format(Series[series_type].value, series_type)]
		return prices

	def bollinger_check(self, api_res):
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
	def __init__(self, name):
		self.api_url = 'https://www.alphavantage.co/query?'
		self.name = name
		name_to_func = {
			"MACD":self.macd_check,
			"STOCH":self.stochastic_check,
			"BBANDS":self.bollinger_check
			}
		self.signal_check = name_to_func[name]




