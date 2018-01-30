#!/usr/bin/env python

'''The code module, containing the app factory function.'''

import os

from flask import Flask, render_template
from flask_cors import CORS

from code.settings import ProdConfig, DevConfig
from code.extensions import (
    db,
    migrate,
)
from code.api import api_blueprint

if os.getenv("FLASK_ENV") == 'prod':
    DefaultConfig = ProdConfig
else:
    DefaultConfig = DevConfig

def create_app(config_object=DefaultConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    # Documentation
    @app.route('/')
    @app.route('/index')
    def index():
        """ Here the user sees the signup and signin gateways """
        return render_template('index.html', title='Home')
    # Enabling cors
    CORS(app)	
    register_extensions(app)
    register_blueprints(app)
    from code.models.user import User
    from code.database import db
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_blueprint)
