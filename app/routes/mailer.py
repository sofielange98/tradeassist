from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_mail import Mail, Message
from app.modules.db import DbConnection
from app import app

bp = Blueprint('mail', __name__, url_prefix='/mail')

mail = Mail(app)

@bp.route("/MailRequest/", methods = ["GET"])
def MailRequest():
	if 'user_id' not in session:
		return 'fail'
	user_id = session['user_id']
	db = DbConnection.getInstance()
	user = db.get_user_by_id(user_id)
	msg = Message('Hello', sender = 'trade.assistant.flask@gmail.com', recipients = user['email'])
	msg.body = "Hello Flask message sent from Flask-Mail"
	mail.send(msg)
	return "Sent"

@bp.route("/Notify/", methods = ["GET"])
def Notify():
	print(request['email'])
	print(request['strategy'])
	if user is not None:
		msg = Message('Hello', sender = 'trade.assistant.flask@gmail.com', recipients = request['email'])
		msg.body = "Hello Flask message sent from Flask-Mail, your strategy had been triggered"
		mail.send(msg)
		return "Sent"
	else:
		return "user doesnt exist"