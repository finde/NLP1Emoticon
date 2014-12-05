from flask import Blueprint, render_template

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/login')
@home.route('/register')
def homepage():
    return render_template('base.html')
