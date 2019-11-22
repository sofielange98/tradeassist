import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.db import DbConnection
from app.modules.User import User 

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/ViewStrategies', methods=('GET', 'POST'))
def ViewStrategies():
	user = g.user 
	if user is not None:
		strategies = DbConnection.getInstance().get_user_strategies(user)
		if strategies is not None:
			return render_template('user_strategies.html', strategies = strategies)
		else:
			flash('Please add some strategies in order to view them')
			return render_template('edit_strategies.html')
	else:
		flash('Please login to view strategies')
		return render_template('auth/login.html')

@bp.route('/EditStrategies', methods=('GET', 'POST'))
def EditStrategies():
	db = DbConnection.getInstance()
	user = g.user 
	if user is not None:
		user.strategies = db.get_user_strategies(user)
		all_strategies = db.get_strategies()
		all_symbols = db.get_symbols()
		
		if request.method == "POST":
			action = request.form['button']
			print(action)
			if action == 'Delete':
				print(request.form)
				db.delete_user_strategy(request.form['strat_id'])
				flash("Deleted Successfully")
				user.strategies = db.get_user_strategies(user)
			
			elif action == 'Update':
				db.update_user_strategy(request.form['strat_id'], request.form)
				flash("Update Success")
				user.strategies = db.get_user_strategies(user)

		return render_template('edit_strategies.html', strategies = user.strategies, available_strategies = all_strategies, available_symbols = all_symbols)
	else:
		return render_template('index.html')	
@bp.route('/AddStrategy', methods=('GET', 'POST'))
def AddStrategy():
	db = DbConnection.getInstance()
	user = g.user 
	print(request)
	if user is not None:
		user.strategies = db.get_user_strategies(user)
		all_strategies = db.get_strategies()
		all_symbols = db.get_symbols()
		
		if request.method == 'GET':
			return render_template('edit_strategies.html', strategies = user.strategies, available_strategies = all_strategies, available_symbols = all_symbols)
		
		elif request.method == 'POST':
			if not user.check_strategy_exists(request.form):
				flash('Success!')
				db.add_strategy(request.form,user)
				user.strategies = db.get_user_strategies(user)
				return render_template('edit_strategies.html', strategies = user.strategies, available_strategies = all_strategies, available_symbols = all_symbols)
			else:
				flash("Already Added That")
				return render_template('edit_strategies.html', strategies = user.strategies, available_strategies = all_strategies, available_symbols = all_symbols)
