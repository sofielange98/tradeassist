from flask_mail import Mail, Message
from flask import current_app, g
from app import app 

class Mailer:
	def __init__(self):
		with app.app_context():
			self.mail = Mail(current_app)
					


	def create_email(self, params):
		notification = '''
		The {} indicator has triggered a {} signal for the symbol {}.

		Happy Trading!
		'''.format(params['strategy'], params['status'], params['symbol'])

		return notification

	def notify(self, params):
		with app.app_context():
			msg = Message('Time to Trade', sender = 'trade.assistant.flask@gmail.com', recipients = [params['email']])
			msg.body = self.create_email(params)

			self.mail.send(msg)
			return "Sent"