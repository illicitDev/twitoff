"""Prediction of Users based on Tweet Embeddings"""
import numpy as np 
from sklearn.linear_model import LogisticRegression
from .model import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet):
    """Determine who is more likley to say a hypothetical tweet"""
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertically stack embeddings
    vects = np.vstack([user0_vects, user1_vects])

    # collection of labels same length as vects
    labels = np.concatenate([np.zeros(len(user0.tweets)). np.ones(len(user1.tweets))])

    # train regression model 
    log_reg = LogisticRegression().fit(vects,labels)

    # vectorize hypo tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet)

    # retrun prediction
    return log_reg.predict(np.array(hypo_tweet_vect).reshape(1, -1))
