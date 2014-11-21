import csv
import sys
import pdb
from pprint import pprint

'''Feature extraction class'''


class TSV_Object:
    # Store tsv object
    # One TSV object per tweet
    def __init__(self, tsv_object, data_type, emotion):
        self.data_type = data_type
        self.emotion = emotion
        self.tsv_object = tsv_object
        self.text = tsv_object[0]
        self.hashtags = tsv_object[1]

    # self.emoticons = tsv_object[2]

    # Get raw text from tsv object
    def get_text(self):
        return self.text

    # Get emoticons from tsv object
    def get_emoticons(self):
        emoticons = []
        emoticons_array = self.emoticons.split(',')
        for emo in emoticons_array:
            print 'emo: ', emo
            emoticons.append(emo)
        return emoticons

    # Get hashtags from tsv object
    def get_tags(self):
        tags = []
        hashtags = self.hashtags.split(',')
        for tag in hashtags:
            print 'tag: ', tag
            tags.append(tag)
        return tags


class TSV_Getter:
    def __init__(self, filename, verbose=0):
        self.all_tsv_objects = []
        print filename
        if "ubuntu" in filename:
            data_type = "ubuntu"
        elif "twitter" in filename:
            data_type = "twitter"
        else:
            data_type = "unknown"

        if "positive-negative" in filename:
            emotion = "mixed"
        elif "positive" in filename:
            emotion = "positive"
        elif "negative" in filename:
            emotion = "negative"
        elif "neutral" in filename:
            emotion = "neutral"
        else:
            emotion = "unknown"

        # Read TSV file:
        with open(filename, 'rb') as tsvIn:
            tsvIn = csv.reader(tsvIn, delimiter='\t')
            for row in tsvIn:
                # Do not store the first row
                if (row[0] == 'Text'):
                    continue
                # Create tsv object of row (which is one tweet)
                tsv_obj = TSV_Object(row, data_type, emotion)
                # Store all tsv objects of this file in this getter class
                self.all_tsv_objects.append(tsv_obj)

    def get_all_tsv_objects(self, size=None):
        if size is None:
            size = len(self.all_tsv_objects)
        return self.all_tsv_objects[0:size]


if __name__ == "__main__":
    dataPoints = [[_.text, _.hashtags, ':('] for _ in TSV_Getter('negative.tsv').get_all_tsv_objects()]
    dataPoints = dataPoints + [[_.text, _.hashtags, ':)'] for _ in TSV_Getter('positive.tsv').get_all_tsv_objects()]
    print len(dataPoints)