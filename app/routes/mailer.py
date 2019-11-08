from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_mail import Mail, Message
from app import app

bp = Blueprint('mail', __name__, url_prefix='/mail')

mail = Mail(app)

@bp.route("/MailRequest/<userid>", methods = ["GET"])
def MailRequest(userid):
	msg = Message('Hello', sender = 'trade.assistant.flask@gmail.com', recipients = ['sofie.lange.98@gmail.com'])
	msg.body = "Hello Flask message sent from Flask-Mail"
	mail.send(msg)
	return "Sent"