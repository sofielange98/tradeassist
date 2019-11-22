from app import app
from flask import render_template

@app.route('/')
@app.route('/Home')
@app.route('/TradeAssist')
@app.route('/index')
def home():
    return(render_template('index.html'))
