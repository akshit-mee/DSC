import tweepy
import pandas as pd
import numpy as np
import sys
from slacker import Slacker
import datetime
from datetime import timezone
import re

# Twitter credentils remove before GITHUB
CONSUMER_KEY = 'r31kBo3wl6XRx6Ev1VCVx'
CONSUMER_SECRET = 'l1bHXu6mDBhkhMA00sFDVrBKBlzYpKtbWa6'
ACCESS_TOKEN = '2407718186-iUj9NpRC9NxAhz10jbj8zYezim'
ACCESS_SECRET = '0rJVp4j5bFk1nbNFoAc2fhLEBZKFLV34R8M'
slack = Slacker('xoxb-10556560388466-euaQDZpyaHrUAjZRpQnpMKyE')


def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

twt = 'Every3Minutes'
domain = 'https://twitter.com/every3minutes'
extractor = twitter_setup()


tweets = extractor.user_timeline(screen_name=twt, count=200)
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])


data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['text'] = np.array([tweet.text for tweet in tweets])
created_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=3)

data = data[(data['Date'] > created_time) & (data['Date'] < datetime.datetime.utcnow())]

slack.chat.post_message('#bot',data['Tweets'])
