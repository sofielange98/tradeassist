import sqlite3
import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
from app import app 

class DbConnection:
    __instance = None
    @staticmethod 
    def getInstance():
        if DbConnection.__instance == None:
            DbConnection()
        return DbConnection.__instance
    def __init__(self):
        if DbConnection.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DbConnection.__instance = self
            print("Connecting to database")
            with app.app_context():
                self.db = sqlite3.connect(
                        current_app.config['DATABASE'],
                        detect_types=sqlite3.PARSE_DECLTYPES,
                        check_same_thread=False
                    )
                self.db.row_factory = sqlite3.Row

    def __del__(self):
        print("Closing database connection")
        self.db.close()

    def insert_new_user(self, user):
        self.db.execute(
                'INSERT INTO USER (email, username, password) VALUES (?, ?, ?)',
                (user.email, user.username, user.password)
            )
        self.db.commit()
        user_id = self.db.execute(
            'SELECT id FROM user WHERE email = ?', (user.email,)
            ).fetchone()
        print(user_id[0])
        for i in range(len(user.indicators)):
            print([user.indicators[i]])
            strat_id = self.db.execute(
                'SELECT id FROM STRATEGIES where name =?',([user.indicators[i]])
                ).fetchone()
            print(strat_id)
            symbol_id = self.db.execute(
                'SELECT id FROM symbols where symbol = ?',([user.symbols[i]])
                ).fetchone()
            self.db.execute(
                    'INSERT INTO USER_STRATEGIES (user_id, strat_id,symbol_id,interim) VALUES (?,?,?,?)',
                    (user_id[0], strat_id[0],symbol_id[0],user.frequencies[i])
                )
        self.db.commit()
        return user_id[0]

    def check_existing_user(self, user):
        if self.db.execute(
            'SELECT id FROM USER WHERE email = ?', (user.email,)
        ).fetchone() is not None:
            return True
        else:  
            return None

    def get_user_by_email(self, email):
        user = self.db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        print(user)
        if user != None:
            user = {
                'username': user['username'],
                'email': user['email'],
                'id':user['id']
                }
        return(user)

    def get_user_by_id(self, id):
        user = self.db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        print(user)
        if user != None:
            user = {
                'username': user['username'],
                'email': user['email'],
                'id':user['id'],
                'password':user['password']
                }
        return(user)

    def get_user_strategies(self,user):
        info = self.db.execute(
            ("SELECT "
                "USER_STRATEGIES.id, STRATEGIES.name, SYMBOL.symbol, USER_STRATEGIES.interim "
                "from "
                "USER_STRATEGIES "
                "INNER JOIN STRATEGIES on STRATEGIES.id = USER_STRATEGIES.strat_id "
                "INNER JOIN SYMBOLS as SYMBOL on SYMBOL.id = USER_STRATEGIES.symbol_id "
                "WHERE USER_STRATEGIES.user_id = ?"), (user.id,)
            ).fetchall()
        return info

    def get_symbols(self):
        available_symbols = self.db.execute(
        'SELECT symbol from SYMBOLS'
        ).fetchall()
        return([s[0] for s in available_symbols])

    def get_full_symbols(self):
        available_symbols = self.db.execute(
        'SELECT symbol from SYMBOLS'
        ).fetchall()
        return([s[0] for s in available_symbols])

    def get_strategies(self):
        available_strategies = self.db.execute(
        'SELECT name from STRATEGIES'
        ).fetchall()
        return([s[0] for s in available_strategies])

    def get_all_user_strategies(self):
        info = self.db.execute(
            ("SELECT " 
            "USER_STRATEGIES.id, STRATEGIES.name, SYMBOLS.symbol, USER.email, USER_STRATEGIES.last_check, USER_STRATEGIES.interim "
            "from "
            "USER_STRATEGIES "
            "INNER JOIN STRATEGIES on STRATEGIES.id = USER_STRATEGIES.strat_id "
            "INNER JOIN SYMBOLS on SYMBOLS.id = USER_STRATEGIES.symbol_id "
            "INNER JOIN USER on USER.id = USER_STRATEGIES.user_id;")
            ).fetchall()
        return info

    def add_strategy(self, strat, user):
        print(strat)
        strat_id = self.db.execute(
                'SELECT id FROM STRATEGIES where name =?',(strat['strategy'],)
                ).fetchone()
        print(strat_id)
        symbol_id = self.db.execute(
                'SELECT id FROM symbols where symbol = ?',(strat['symbol'],)
                ).fetchone()
        self.db.execute(
                    'INSERT INTO USER_STRATEGIES (user_id, strat_id,symbol_id,interim) VALUES (?,?,?,?)',
                    (user.id, strat_id[0],symbol_id[0],strat['frequency'])
                )
        self.db.commit()

    def delete_user_strategy(self, strat_id):
        self.db.execute(
            'DELETE from USER_STRATEGIES where id =?',(strat_id,)
            )
        self.db.commit()

    def update_user_strategy(self, sid, new_strat):
        strat_id = self.db.execute(
                'SELECT id FROM STRATEGIES where name =?',(new_strat['strategy'],)
                ).fetchone()
        symbol_id = self.db.execute(
                'SELECT id FROM symbols where symbol = ?',(new_strat['symbol'],)
                ).fetchone()
        self.db.execute(
            'UPDATE USER_STRATEGIES set strat_id=?, interim=?, symbol_id=? where id = ?',(strat_id[0], new_strat['frequency'],symbol_id[0], sid)
            )
        self.db.commit()
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    print("Closing db connection")
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('db_init.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
