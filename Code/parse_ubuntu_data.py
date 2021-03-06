import csv
import re
import sys
from MultilayerPerceptron import mlp_predict
import requests, json

from info import classify2
from math import e
import pickle
from datetime import datetime


class MyDict(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
        return 0


pos = MyDict()
neg = MyDict()
totals = [0, 0]


def percentage_confidence(conf):
    return 100.0 * e ** conf / (1 + e ** conf)


def get_sentiment_info(text):
    flag, confidence = classify2(text, pos, neg, totals)
    if confidence > 0.5:
        sentiment = "positive" if flag else "negative"
    else:
        sentiment = "neutral"
    conf = "%.4f" % percentage_confidence(confidence)
    return sentiment, conf


def parse_emoticons(emoticons):
    obj = {}

    for emo in emoticons:
        join_symbols = []

        for symbol in emoticons[emo]:
            pattern = re.escape(symbol)
            join_symbols.append(pattern)

        obj[emo] = "|".join(join_symbols)

    return obj


def clean_string(raw):
    try:
        string = raw.encode('utf-8').replace('\n', '').replace('\r', '')
    except Exception as inst:
        string = raw.replace('\n', '').replace('\r', '')

    return string


def remove_url(text):
    return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '@HLINK', text)


def parse_data(filename, emoticons):
    emos = parse_emoticons(emoticons)

    folder_name = '../Data/Chat Data/'
    file_in = folder_name + filename + ".txt"
    file_out = folder_name + filename + ".tsv"

    with open(file_in, 'rb') as txt, open(file_out, 'wb') as tsv:
        tsv = csv.writer(tsv, delimiter="\t", lineterminator='\n')

        for row in txt:
            # regular expression
            match_timestamp = re.match('^(\[[^\]]*\]){1}', row)
            match_username = re.search('<[^>]*>', row)
            match_message = re.split('^((\[[^\]]*\]){1}[ ]{1}(<[^>]*>){1}[ ]{1}){1}', row)

            if match_timestamp and match_username and len(match_message) == 5:
                timestamp = match_timestamp.group(0)

                username = match_username.group(0)

                message = clean_string(match_message[4])
                message = remove_url(message)

                # regular expression for emoticon
                label = "neutral"

                for emo in emos:
                    match_emo = re.search(emos[emo], message)

                    if match_emo:
                        label = emo
                        break

                if label == "neutral":
                    new_label, confidence = get_sentiment_info(message)
                    print label, new_label, confidence, message
                    label = new_label

                label = "[" + label + "]"

                row_tsv = [label, timestamp, username, message]
                try:
                    tsv.writerow(row_tsv)
                except Exception as inst:
                    print "There is an error when writing tsv file"
                    sys.exit()


filename = [
    "2006-05-27-#ubuntu",
    "2006-06-01-#ubuntu",
    "2007-04-20-#ubuntu",
    "2007-04-21-#ubuntu",
    "2007-04-22-#ubuntu",
    "2007-10-19-#ubuntu",
    "2007-10-20-#ubuntu",
    "2007-10-21-#ubuntu",
    "2008-04-25-#ubuntu",
    "2008-04-26-#ubuntu",
]

emoticons = {
    'positive': [
        ":)", ":-)", ":)", ":D", ":o)", ":]", ":3", ":c)", ":>", ":}", ":^)", ":-D",
        ";)", ";-)", ";)", ";D", ";o)", ";]", ";3", ";c)", ";>", ";}", ";^)", ";-D",
        "=)", "=]", "8)", "( '}{' )", "*-)", "*)",
        " 8-D", " 8D", " x-D", " xD", " X-D", " XD", " =-D", " =D", " =-3", " =3", " B^D",
        ":-))", ":'-)", ":')",
        ";-))", ";'-)", ";')",
        " X-P", " x-p", " xp", " XP", " xP", "=p",
        ":*", ":^*", ";)", ":-]", ";D", ";^)", ":-",
        ":*", ":^*", ";)", ";-]", ";D", ";^)", ";-",
        ">:P", ":-P", ":P", ":-p", ":p", ":-P",
        ">;P", ";-P", ";P", ";-p", ";p", ";-P",
        ":P", ":p", ":-p", ":-b", ":b", " d:",
        ";P", ";p", ";-p", ";-b", ";b", " d;",
        "^o^", "^.^", "^_^"
    ],
    'negative': [
        ":(", ":'(",
        ";(", ";'(",
        ">:[", ":-(", ":(", ":-c", ":c", ":-<", ":<", ":-[", ":[", ":{",
        ">;[", ";-(", ";(", ";-c", ";c", ";-<", ";<", ";-[", ";[", ";{",
        ":-||", ":@ >:(",
        ";-||", ";@ >;(",
        ":'-(", ":'(",
        ";'-(", ";'(",
        " T_T"
        " D:<", " D:", " D-':",
        " D;<", " D;", " D-';",
        " D8", " D=", " DX", " v.v", "=/", "=\\", "=L", ">.<",
        ">:\\", ">:/", ":-/", ":-.", ":/", ":\\", ":L", ":S",
        ">;\\", ">;/", ";-/", ";-.", ";/", ";\\", ";L", ";S",
        ":$",
        ";$",
    ]
}

pos, neg, totals = pickle.load(open('reduceddata.pickle'))

for f in filename:
    parse_data(f, emoticons)