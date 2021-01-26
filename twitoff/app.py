"""Main app/routing for TwitOff"""
from os import getenv
from flask import Flask, render_template
from .model import *
from .twitter import *


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)
    
    @app.route('/')
    def root():
        return render_template('base.html', title="Home")

    @app.route('/update')
    def update():
        add_or_update_user('elonmusk')
        return render_template('base.html', title="Home")

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Home")

    return app
