"""SQLAlchemy models and utility functions for TwitOff"""
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

class User(DB.Model):
    """Twitter Users corresponfing to Tweets"""
    # Columns in User table
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)
    
    def __repr__(self):
        return f'<User: {self.name}>'


class Tweet(DB.Model):
    """Tweets corresponding to Users"""
    # Columns in Tweet table
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, 
        DB.ForeignKey('user.id'), nullable=False)
    # creates user link between tweets
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet: {self.text}>'


