__author__ = 'finde'

import json
import csv


def text_cleaner(text):
    return text.encode('utf-8').replace('\n', ' ').replace('\r', '')

# filename = 'negative_raw'
filename = 'negative'
# filename = 'positive_raw'
# filename = 'positive'
with open(filename + '.json', 'r') as tsvin, open(filename + '.tsv', 'w') as tsvout:
    # tsvin = csv.reader(tsvin, delimiter='\t')
    tsvin = json.load(tsvin)
    tsvout = csv.writer(tsvout, delimiter='\t')

    # todo: write header
    for row in tsvin:
        # basic
        # tsvout.writerow([row.replace('\n', ' ').replace('\r', '').encode('utf-8')])

        # with structure
        tsvout.writerow([text_cleaner(row['text']), ', '.join(row['hashtags']).encode('utf-8')])