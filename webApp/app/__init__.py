import os

from flask import Flask
from config import config
from extensions import db
from blueprints.home.views import home
from blueprints.auth.views import auth
from blueprints.perceptron.views import perceptron


def register_blueprints(app):
    app.register_blueprint(home)
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(perceptron, url_prefix='/api/perceptron')


def create_app(config_name):
    # # App ##
    app = Flask(__name__, static_folder='static',
                template_folder='templates')

    ## Config ##
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    ## Database ##
    db.init_app(app)
    db.app = app

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify

        sslify = SSLify(app)

    ## Blueprints ##
    register_blueprints(app)

    return app
