__author__ = "Finde"
__version__ = "v0.1"

import json
import tweepy
from EmotionalProject import DataPoint  # source = http://www.tweepy.org/, pip install tweepy
import \
    language_check  # source = https://pypi.python.org/pypi/language-check, pip install --user --upgrade language-check

# tweepy
consumer_key = 'Ltcqzn4LYuxhDWjDYvAplZdX6'
consumer_secret = 'EQlZTaU9kWvC5aAT2RbM1PjIk1HhrmQaWzoWuHP8lWlmrJkdPN'
access_token = '123835904-UAHBaeePOY7FRpj70GA3FvfrCLkxBKeQbSiqxPT1'
access_token_secret = '6tYsNUf9whpzpxiSGSDXWLjIZb4SZ55OWTrhSiKZYJpeO'

# language_check
lang_tool = language_check.LanguageTool('en-US')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

query = ':)'
max_tweets = 100

dataPoints = []

searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)];

for tweet in searched_tweets:
    # data_string, hashtags, class_label
    status = DataPoint(tweet.text, [1, 2], 'asd')
    # status.text = tweet.text;

    dataPoints.append(status)

    print status.get_data_string()
    # print lang_tool.check(tweet)
    # print tweet.text

print len(dataPoints)
# print analyze_tweet('yeah... right..');
