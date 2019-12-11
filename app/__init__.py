import os

from flask import Flask
from flask_apscheduler import APScheduler
from datetime import datetime

import requests
import json

from app.rand_curr import get_random_currency

class Config(object):
    JOBS = [
        {
            'id': 'check',
            'func': 'app:check',
            'trigger': 'interval',
            'days': 1,
            'start_date':datetime.today().replace(hour=22)
        },
        {
            'id': 'demo_check',
            'func': 'app:demo_check',
            'trigger': 'interval',
            'seconds': 20,
            
        }
    ]

    SCHEDULER_API_ENABLED = True
    SECRET_KEY='dev'
    ALPHA_API_KEY = 'EKO46GFZF2SFKBM7'
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'trade.assistant.flask@gmail.com'
    MAIL_PASSWORD = 'Stocks5678*'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # I'm gonna have the app get forex exchange rates every 5 seconds and give them to me


app = Flask(__name__)

    #scheduler set up
app.config.from_object(Config())

    #database set up
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
app.config['DATABASE'] = os.path.join(app.instance_path, 'tradeassist.sqlite')


from app.modules.DailyCheck import DailyChecker
def check():
    print("Checking")
    checker = DailyChecker()
    checker.execute()
    #routing for requests
from flask_mail import Mail, Message
mail = Mail(app)

def get_exchange():
    phys_currency, dig_currency = get_random_currency()
    params = {
            'apikey' : 'EKO46GFZF2SFKBM7',
            'from_currency' : phys_currency,
            'to_currency': dig_currency,
            'function' : 'CURRENCY_EXCHANGE_RATE'
    }

    resp = requests.get(url = 'https://www.alphavantage.co/query?', params = params)
    print(resp.status_code)
    if resp.status_code == 200: # OK
        s = json.dumps(resp.json())
        y = json.loads(s)
        if 'Note' in y:
            return 'none'
    return y
def demo_check():

# https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo
    y = get_exchange()
    print(y)
    while y["Realtime Currency Exchange Rate"]['8. Bid Price'] == '-':
        y = get_exchange()
    print(y)
    if y == 'none': 
        return

    from_name = y["Realtime Currency Exchange Rate"]['2. From_Currency Name']
    to_name = y["Realtime Currency Exchange Rate"]['4. To_Currency Name']
    phys_currency = y["Realtime Currency Exchange Rate"]['1. From_Currency Code']
    dig_currency = y["Realtime Currency Exchange Rate"]['3. To_Currency Code']
    bid = y["Realtime Currency Exchange Rate"]['8. Bid Price']
    ask = y["Realtime Currency Exchange Rate"]['9. Ask Price']
        
    message = '''
        From Currency: {}
        To Currency: {}
        Current Bid Price for {}/{} Exchange Rate: {}

        Current Ask Price for {}/{} Exchange Rate: {}

        Happy Trading!
        '''.format(from_name, to_name,phys_currency, dig_currency, bid, phys_currency, dig_currency, ask)

    with app.app_context():

        msg = Message('Exchange Rates', sender = 'trade.assistant.flask@gmail.com', recipients = ['sofie.lange.98@gmail.com'])
        msg.body = message

        mail.send(msg)

with app.app_context():
    # from app.modules.db import DbConnection
    # DbConnection().

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    from app.routes import mailer
    app.register_blueprint(mailer.bp)

from app.modules.Strategy import Strategy

from app.routes import auth
app.register_blueprint(auth.bp)

from app.routes import home
app.register_blueprint(home.bp)

from app.routes import info
app.register_blueprint(info.bp)

from app.routes import account
app.register_blueprint(account.bp)
    