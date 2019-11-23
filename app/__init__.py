import os

from flask import Flask
from flask_apscheduler import APScheduler

class Config(object):
    JOBS = [
        {
            'id': 'check',
            'func': 'app:check',
            'trigger': 'interval',
            'days': 1,
            
        }
        # {
        #     'id': 'job1',
        #     'func': 'app:job1',
        #     'args': (1, 2),
        #     'trigger': 'interval',
        #     'seconds': 20,
            
        # }
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

# def job1(a,b):
#     print(a,b)


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

with app.app_context():
    from app.modules.db import DbConnection
    DbConnection()

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    from app.routes import mailer
    app.register_blueprint(mailer.bp)

from app.routes import auth
app.register_blueprint(auth.bp)

from app.routes import home
app.register_blueprint(home.bp)

from app.routes import info
app.register_blueprint(info.bp)

from app.routes import account
app.register_blueprint(account.bp)
    



