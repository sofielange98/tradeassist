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
            with app.app_context():
                print("Connecting to database")
                self.db = sqlite3.connect(
                    current_app.config['DATABASE'],
                    detect_types=sqlite3.PARSE_DECLTYPES,
                    check_same_thread=False
                )
                self.db.row_factory = sqlite3.Row
    def __del__(self):
        print("Closing database connection")
        self.db.close()

def get_db():
    if 'db' not in g:
        print("Connecting to database")
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
