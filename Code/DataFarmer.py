import os
import json
import re
import numpy as np
from time import sleep
import tweepy  # http://www.tweepy.org/
import progressbar


class DataFarmer:
    def __init__(self, twitter_config):
        self.twitter_config = twitter_config
        auth = tweepy.OAuthHandler(self.twitter_config['consumer_key'], self.twitter_config['consumer_secret'])
        auth.set_access_token(self.twitter_config['access_token'], self.twitter_config['access_token_secret'])
        self.twitter_api = tweepy.API(auth)

    def uniqify(self, seq, idfun=None):
        # order preserving
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            # in old Python versions:
            # if seen.has_key(marker)
            # but in new ones:
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result

    def match_emotion(self, text, emotion):
        my_compile = lambda pat: re.compile(pat, re.UNICODE)

        normal_eyes = r'[:=]'
        nose_area = r'(|o|O|-)'

        happy_mouths = r'[D\)\]]'
        sad_mouths = r'[\(\[]'

        happy_re = my_compile('(\^_\^|' + normal_eyes + nose_area + happy_mouths + ')')
        sad_re = my_compile(normal_eyes + nose_area + sad_mouths)

        h = happy_re.search(text)
        s = sad_re.search(text)

        # TODO:: remove emoticon

        # both happy and sad
        if h and s:
            return False

        # happy found
        if h and emotion == 'positive':
            return True

        # sad found
        if s and emotion == 'negative':
            return True

        # sad nothing found
        if emotion == 'neutral':
            return True

        # default if all fail
        return False

    def fetch_from_twitter(self, target):
        number_of_tweets = []
        for q in self.twitter_config['query']:
            # file exists, it should append instead of overwrite
            statuses = []
            filename = q['class_label'] + '_raw.json'
            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                # load json dump into variable
                # TODO: error handling if the file is not a valid JSON
                f = open(filename, 'r+')
                statuses = json.load(f)
                f.close()

            n_tweet = len(statuses)

            if n_tweet < target:

                # twitter crawler
                max_tweets_per_query = self.twitter_config['max_tweets_per_query']
                search = self.twitter_api.search

                searched_tweets = [status for status in
                                   tweepy.Cursor(search, q=q['query_string'], lang='en').items(max_tweets_per_query)]

                for tweet in searched_tweets:

                    if len(self.uniqify(statuses)) >= target:
                        break

                    raw_text = tweet.text.encode('utf8')

                    # basic pre-processing to ensure the status match with the target emotion
                    # and only one emotion (class_label) allowed per status (no mixed emotions)
                    if not self.match_emotion(raw_text, q['class_label']):
                        continue

                    statuses.append(raw_text)

                statuses = self.uniqify(statuses)

                f = open(filename, 'w+')

                # store unique status
                f.write(json.dumps(statuses, sort_keys=True, indent=4, separators=(',', ': ')))
                f.close()
                # print '============================================'
                # print ' Emoticon: ', q['class_label']
                # print ' Query: ', q['query_string']
                # print ' New tweets: ', (len(statuses) - n_tweet)
                # print ' Total tweets: ', len(statuses)
                # print '============================================'

            number_of_tweets.append(len(statuses))

        return number_of_tweets

    def run(self, target):
        bar = progressbar.ProgressBar(maxval=target,
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        number_of_tweets = self.fetch_from_twitter(target)
        bar.update(np.mean(number_of_tweets))

        while len(number_of_tweets) > 0 and np.mean(number_of_tweets) < target:
            sleep(10)
            number_of_tweets = self.fetch_from_twitter(target)
            bar.update(np.mean(number_of_tweets))

        bar.finish()


if __name__ == "__main__":
    twitter_cfg = {
        # fin
        'consumer_key': 'Ltcqzn4LYuxhDWjDYvAplZdX6',
        'consumer_secret': 'EQlZTaU9kWvC5aAT2RbM1PjIk1HhrmQaWzoWuHP8lWlmrJkdPN',
        'access_token': '123835904-UAHBaeePOY7FRpj70GA3FvfrCLkxBKeQbSiqxPT1',
        'access_token_secret': '6tYsNUf9whpzpxiSGSDXWLjIZb4SZ55OWTrhSiKZYJpeO',

        # sandra
        # 'consumer_key': 'SVlTKc5HuieEXGyxCldQKwyih',
        # 'consumer_secret': 'XlmXl6cbjdqQ1yp2oTjVaPTtGN64UoWpjSba8tg75pMs8fkP1S',
        # 'access_token': '2864250076-Q4yYb98vZ2mfLVc2nItl651AxKqkZzaJdEAVh7n',
        # 'access_token_secret': 'tFy5NRL4iZUierYdyxcoP0mAp5XcDAHhoRroHd3krT8Q0',

        'max_tweets_per_query': 25,
        'query': [
            {'class_label': 'positive', 'query_string': ':)'},
            {'class_label': 'negative', 'query_string': ':('}
        ]
    }

    data_farmer = DataFarmer(twitter_cfg)
    data_farmer.run(900)