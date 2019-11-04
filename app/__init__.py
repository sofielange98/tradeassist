import os

from flask import Flask

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'tradeassist.sqlite'),
    API_KEY = 'EKO46GFZF2SFKBM7'
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from app.db import DbConnection
DbConnection()

from app import routes

from . import auth
app.register_blueprint(auth.bp)

from . import home
app.register_blueprint(home.bp)

