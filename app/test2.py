from Strategy import Strategy


macd = Strategy("MACD") 
params = {
	"function": "MACD",
	"interval": "daily",
	"symbol": "SPY",
	"series_type": "open",
}
res = macd.check_status(params)
params = {
	"function": "STOCH",
	"interval": "daily",
	"symbol": "SPY",
	"series_type": "open",
}
stoch = Strategy("STOCH") 

res = stoch.check_status(params)

params = {
	"function": "BBANDS",
	"interval": "daily",
	"symbol": "SPY",
	"series_type": "close",
	"time_period":"60"
}

bbands = Strategy("BBANDS")
res = bbands.check_status(params)