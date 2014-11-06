__author__ = "Finde"
__version__ = "v0.1"

import json
import tweepy  # source = http://www.tweepy.org/, pip install tweepy
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

searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, lang='en').items(max_tweets)]

filename = 'data.json'
file = open(filename, 'w+')

# file.write('[')
for tweet in searched_tweets:
    # data_string, hashtags, class_label

    status = {}
    status['raw'] = tweet.text

    # preprocessing
    status['text'] = tweet.text
    status['emoticons'] = tweet.text
    status['tags'] = tweet.text

    # print status.get_data_string()
    # print lang_tool.check(tweet)
    # print tweet.text
    dataPoints.append(status)

file.write(json.dumps(dataPoints))
# file.write(']')
file.close()

# data = json.load(open(filename))

# with open('data.json', 'wb') as fp:
#     json.dump(dataPoints, fp)