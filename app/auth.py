import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import DbConnection

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    db = DbConnection.getInstance().db 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        indicators = request.form.getlist('indicator')
        frequencies = []
        symbols = []
        for indicator in indicators:
            frequencies.append(request.form[indicator+'_frequency'])
            symbols.append(request.form[indicator + '_symbol'])
        print(request.form)
        print(indicators)
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = "Email is required."
        elif db.execute(
            'SELECT id FROM USER WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO USER (email, username, password) VALUES (?, ?, ?)',
                (email, username, generate_password_hash(password))
            )
            db.commit()
            user_id = db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
            ).fetchone()
            print(user_id)
            for i in range(len(indicators)):
                print([indicators[i]])
                strat_id = db.execute(
                'SELECT id FROM STRATEGIES where name =?',([indicators[i]])
                ).fetchone()
                print(strat_id)
                symbol_id = db.execute(
                'SELECT id FROM symbols where symbol = ?',([symbols[i]])
                ).fetchone()
                db.execute(
                    'INSERT INTO USER_STRATEGIES (user_id, strat_id,symbol_id,interim) VALUES (?,?,?,?)',
                    (user_id[0], strat_id[0],symbol_id[0],frequencies[i])
                )
                db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    available_symbols = db.execute(
        'SELECT symbol from SYMBOLS'
        ).fetchall()
    available_strategies = db.execute(
        'SELECT name from STRATEGIES'
        ).fetchall()
    print([s[0] for s in available_symbols])
    available_symbols = [s[0] for s in available_symbols]
    available_strategies = [s[0] for s in available_strategies]
    return render_template('auth/register.html', available_strategies = available_strategies, available_symbols = available_symbols)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = DbConnection.getInstance().db
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            user_info = db.execute(
            ("SELECT "
                "STRATEGIES.name, SYMBOL.symbol, USER_STRATEGIES.interim "
                "from "
                "USER_STRATEGIES "
                "INNER JOIN STRATEGIES on STRATEGIES.id = USER_STRATEGIES.strat_id "
                "INNER JOIN SYMBOLS as SYMBOL on SYMBOL.id = USER_STRATEGIES.symbol_id "
                "WHERE USER_STRATEGIES.user_id = ?"), (user['id'],)
            ).fetchall()
                       
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
