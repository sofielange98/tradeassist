from app import app
from flask import render_template

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'
@app.route('/')
@app.route('/Home')
@app.route('/TradeAssist')
@app.route('/index')
def home():
    return(render_template('index.html'))
