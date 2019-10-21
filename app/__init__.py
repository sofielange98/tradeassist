import os

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'tradeassist.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from db import DbConnection
DbConnection()

from app import routes

from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import home
app.register_blueprint(home.bp)

