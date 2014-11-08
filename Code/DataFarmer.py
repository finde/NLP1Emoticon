__author__ = "Finde"
__version__ = "v0.1"

import os
import json
import re
import tweepy  # http://www.tweepy.org/

import language_check  # https://pypi.python.org/pypi/language-check
import nltk  # http://www.nltk.org/
from nltk.tokenize.punkt import PunktWordTokenizer


def uniqify(seq, idfun=None):
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


class Preprocessor:
    def __init__(self, text):
        print text
        self.text = text
        self.lang_tool = language_check.LanguageTool('en-US')

    def language_corrector(self, text):
        matches = self.lang_tool.check(text)
        return language_check.correct(text, matches)

    def remove_html(self, text):
        return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '@HLINK', text)

    def remove_retweet(self, text):
        if text.find("RT ") == 0:
            return text.replace("RT ", "")
        return text

    def get_object(self):
        status = {}
        status['hashtags'] = re.findall(r"#(\w+)", self.text)

        status['text'] = self.text
        # replace HTML link with @HLINK
        status['text'] = self.remove_html(status['text'])

        # spellchecker
        status['text'] = self.language_corrector(status['text'])

        # remove RT
        status['text'] = self.remove_retweet(status['text'])

        return status


class DataFarmer:
    def __init__(self, twitter_config):
        self.twitter_config = twitter_config
        auth = tweepy.OAuthHandler(self.twitter_config['consumer_key'], self.twitter_config['consumer_secret'])
        auth.set_access_token(self.twitter_config['access_token'], self.twitter_config['access_token_secret'])
        self.twitter_api = tweepy.API(auth)

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

    def run_twitter_crawler(self):

        for q in self.twitter_config['query']:

            max_tweets_per_query = self.twitter_config['max_tweets_per_query']
            search = self.twitter_api.search

            searched_tweets = [status for status in
                               tweepy.Cursor(search, q=q['query_string'], lang='en').items(max_tweets_per_query)]

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
            for tweet in searched_tweets:
                # print dir(tweet)
                raw_text = tweet.text.encode('utf8')

                # basic pre-processing to ensure the status match with the target emotion
                # and only one emotion (class_label) allowed per status (no mixed emotions)
                if not self.match_emotion(raw_text, q['class_label']):
                    continue

                statuses.append(raw_text)

            f = open(filename, 'w+')

            # store unique status
            statuses = uniqify(statuses)
            f.write(json.dumps(statuses, sort_keys=True, indent=4, separators=(',', ': ')))
            f.close()
            print '============================================'
            print ' Emoticon: ', q['class_label']
            print ' Query: ', q['query_string']
            print ' New tweets: ', (len(statuses)-n_tweet)
            print ' Total tweets: ', len(statuses)
            print '============================================'

    def run_preprocess(self):
        for q in self.twitter_config['query']:
            statuses = []
            filename = q['class_label'] + '_raw.json'
            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                # load json dump into variable
                f = open(filename, 'r+')
                statuses = json.load(f)
                f.close()

            # for each status, run cleaner again
            new_statuses = []
            for status in statuses:
                # not done here
                status['text'] = Preprocessor(status['raw']).get_text()
                new_statuses.append(status)

            f = open(filename, 'w+')
            f.write(json.dumps(new_statuses))
            f.close()


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

        'max_tweets_per_query': 50,
        'query': [
            {'class_label': 'positive', 'query_string': ':)'},
            {'class_label': 'negative', 'query_string': ':('}
        ]
    }

    data_farmer = DataFarmer(twitter_cfg)
    data_farmer.run_twitter_crawler()