import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import DbConnection
from app.User import User 

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = DbConnection.getInstance()
    if request.method == 'POST':
        user = User(request.form)
        
        if db.check_existing_user(user) != None:
            error = 'Email {} is already registered.'.format(user.email)

        if user.error is None:
            db.insert_new_user(user)
            return redirect(url_for('auth.login'))

        flash(error)
    available_symbols = db.get_symbols()
    available_strategies = db.get_strategies()
    print([s[0] for s in available_symbols])
    available_symbols = [s[0] for s in available_symbols]
    available_strategies = [s[0] for s in available_strategies]
    return render_template('auth/register.html', available_strategies = available_strategies, available_symbols = available_symbols)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = DbConnection.getInstance()
        error = None
        user = db.get_user_by_email(email)
        user['password'] = password
        user = User(user)
        if user is None:
            error = 'Incorrect email.'
        elif not user.valid_user_password(password):
            error = 'Incorrect password.'
        print(error)
        if error is None:
            print("Successful login!!")
            session.clear()
            session['user_id'] = user.id
            user_info = db.get_user_strategies(user)
                       
            return render_template('account.html', strategies = user_info)


        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = DbConnection.getInstance().db.execute(
            'SELECT * FROM USER WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
