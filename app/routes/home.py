from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='')

@bp.route('/')
@bp.route('/home')
def home():
    return(render_template('index.html'))
