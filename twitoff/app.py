"""Main app/routing for TwitOff"""
from os import getenv
from flask import Flask, render_template, request
from .model import *
from .twitter import *
from .predict import predict_user


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)
    
    @app.route('/')
    def root():
        return render_template('base.html', title="Home")

    @app.route('/user', methods=['POST'])
    @app.route('/user<name>', methods=['GET'])
    def user(name=None, message=""):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} was successfully added!'
            
            tweets = User.query.filter(User.name == name).one().tweets
        
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        
        return render_template('user.html', title=name, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
                [request.values['in_user0'], request.values['in_user1']])
        
        if user0 == user1:
            message = 'Can\'t comapre users to themselves'

        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = '\'{}\' is more likely to be said by {} than {}.'.format(
                request.values['tweet_text'], 
                user1 if prediction else user0, 
                user0 if prediction else user1
                )

        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/update')
    def update():
        query = User.query.all()

        names = [str(user.name) for user in query]

        DB.drop_all()
        DB.create_all()

        for name in names:
            add_or_update_user(name)

        return render_template('base.html', title="Home")

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="Home")

    return app
