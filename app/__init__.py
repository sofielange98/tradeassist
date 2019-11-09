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
            
        },
        {
            'id': 'job1',
            'func': 'app:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 20,
            
        }
    ]

    SCHEDULER_API_ENABLED = True
    SECRET_KEY='dev'
    ALPHA_API_KEY = 'EKO46GFZF2SFKBM7'

def job1(a,b):
    print(a,b)

def check():
    print("Checking")
    checker = DailyChecker()
    checker.execute()

app = Flask(__name__)

#scheduler set up
app.config.from_object(Config())

#database set up
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
app.config['DATABASE'] = os.path.join(app.instance_path, 'tradeassist.sqlite')

#mailer set up

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'trade.assistant.flask@gmail.com'
app.config['MAIL_PASSWORD'] = 'Stocks5678*'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#routing for requests
from app.modules.db import DbConnection
DbConnection()

#### UNCOMMENT FOR A LOT OF API REQUESTS ####
# from app.modules.DailyCheck import DailyChecker
# checker = DailyChecker()
# checker.execute()

scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
scheduler.init_app(app)

scheduler.start()

from app.routes import routes

from app.routes import auth
app.register_blueprint(auth.bp)

from app.routes import home
app.register_blueprint(home.bp)

from app.routes import info
app.register_blueprint(info.bp)

from app.routes import mailer 
app.register_blueprint(mailer.bp)

from flask_mail import Mail, Message
mail = Mail(app)

@app.route("/MailMe", methods = ["GET"])
def MailMe():
    msg = Message('Hello', sender = 'trade.assistant.flask@gmail.com', recipients = ['sofie.lange.98@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"



