from __future__ import division

import json
import argparse
import re
from string import punctuation
import nltk
import time
import DataPoint
import numpy as np


class TrainingData:
    def __init__(self, data_points):
        self.data_points = data_points
        self.feature_dictionary = {"words": 1,
                                   "negative_words": 2,
                                   "positive_words": 3,
                                   "positive_words_hashtags": 4,
                                   "negative_words_hashtags": 5,
                                   "uppercase_words": 6,
                                   "special_punctuation": 7,
                                   "adjectives": 8}


    #####################
    # Basic class funcs #
    #####################

    def get_training_points(self):
        return self.data_points

    def print_data(self):
        for each in self.data_points:
            each.print_data_point()


        ############################
        # Feature extraction funcs #
        ############################

    def count_words(self):
        return self.count_feature(self.feature_dictionary['words'])

    #### Might be changed to a matrix if it's hard to work with!!
    # Returns a dictionary containing the values corresponding to all
    # the features for all the datapoints.
    def get_feature_dictionary(self):
        d = {}
        for feature in self.feature_dictionary:
            #print 'result for feature ', feature, ': \n', self.count_feature(self.feature_dictionary[feature])
            d[feature] = self.count_feature(self.feature_dictionary[feature])
            print ' == ', feature, ':', d[feature]

        return d

    ''' Returns the feature values for all features for each datapoint
    so 1 vector with all the feature values for 1 datapoint'''

    def get_feature_matrix(self):
        feature_dict = self.get_normalized_feature_dictionary()
        feat_matrix = [[d[i] for d in feature_dict.values()] for i in range(0, len(feature_dict['adjectives']))]

        return feat_matrix

    ''' Returns the label vector '''

    def get_label_vector(self):
        return [each.get_class_label() for each in self.get_training_points()]


    ''' Returns normalized feature dictionary
    All data will be rescaled so each feature has range value [0.1,0.9]'''

    def get_normalized_feature_dictionary(self):
        feature_dict = self.get_feature_dictionary()
        normalized_feature_dict = {}

        for feature in feature_dict:
            feature_values = feature_dict[feature]

            max_value = max(feature_values)
            min_value = min(feature_values)

            denominator = max_value - min_value
            denominator = 1 if denominator == 0 else denominator

            normalized_values = []

            for value in feature_values:
                normalized_value = ((0.9 - 0.1) * (value - min_value) / denominator) + 0.1
                normalized_values.append(normalized_value)

            normalized_feature_dict[feature] = normalized_values

        return normalized_feature_dict


    ########################################
    # Help functions for eature extraction #
    ########################################

    def count_feature(self, feature):
        if feature == self.feature_dictionary['words']:
            return [each.count_words() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['positive_words']:
            return [each.count_positive_words() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['negative_words']:
            return [each.count_negative_words() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['positive_words_hashtags']:
            return [each.count_positive_words_in_hashtags() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['negative_words_hashtags']:
            return [each.count_negative_words_in_hashtags() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['uppercase_words']:
            return [each.count_uppercase_words() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['special_punctuation']:
            return [each.count_special_punctuation() for each in self.get_training_points()]

        elif feature == self.feature_dictionary['adjectives']:
            # if adjectives, then show progress bar, because it is so slooow
            output = []
            for each in self.get_training_points():
                output.append(each.count_adjectives())

            return output

            # one-liner
            # return [each.count_adjectives() for each in self.get_training_points()]

        else:
            return ['unknown feature, bro! :( Give me another one!']


if __name__ == "__main__":

    # Command line arguments
    parser = argparse.ArgumentParser(description="Run simulation")

    parser.add_argument('-text', metavar='The text of the data point', type=str)
    parser.add_argument('-hashtags', metavar='The text of the data point', type=list)
    parser.add_argument('-class', metavar='The class label of the data point (-1, 0, 1)', type=int)

    args = parser.parse_args()

    # If arguments are passed to the command line, assign them.
    # Otherwise, use some standart ones.
    if (vars(args)['text'] is not None):
        data_string1 = vars(args)['text']
    else:
        data_string1 = "What's going on if I Happily try to do this SAD thing?!"

    if (vars(args)['hashtags'] is not None):
        hashtags1 = vars(args)['hashtags']
    else:
        hashtags1 = ["#FeelingProductive", "#LifeIsSoAwesome", "#NLPSUCKS", "#sohappy"]

    if (vars(args)['class'] is not None):
        data_class1 = vars(args)['class']
    else:
        data_class1 = 1

    data_string2 = "This is a second AWesOme example and i LOVE it?!"
    hashtags2 = ["#ProjectBecomesAnnoying", "#MeSoSleepy", "#suicidemood", "#totallyhungry"]

    data_class2 = -1


    # Construct a data point:
    data_point1 = DataPoint.DataPoint(data_string1, hashtags1, data_class1)
    data_point2 = DataPoint.DataPoint(data_string2, hashtags2, data_class2)

    data = [data_point1, data_point2]

    training_data = TrainingData(data)
    # Do some random shit to make sure things work :)

    print "This is your first data point: \n "
    data_point1.print_data_point()
    #print data_point1.get_data_string()
    print "This is your second data point: \n "
    data_point2.print_data_point()
    #print data_point2.get_data_string()
    print "number of words: \n ", training_data.count_words()
    print "feature dictionary: \n ", training_data.get_feature_dictionary()

    feature_dict = training_data.get_feature_dictionary()
    feat_matrix = training_data.get_feature_matrix()  #[[d[i] for d in feature_dict.values()] for i in range(0, len(feature_dict['adjectives']))]
    print 'feat_matrix', feat_matrix

    '''
    print "This is your data splitted: \n ", data_point.split_sentence()
    print "This is your data without punctuation: \n ", data_point.get_sentence_without_punctuation()
    print "The word count is: ", data_point.count_words()
    print "The # of ? and ! is: ", data_point.count_special_punctuation()

    print "Number of positive words: ", data_point.count_positive_words()
    print "Number of negative words: ", data_point.count_negative_words()

    print "Number of uppercase words: ", data_point.count_uppercase_words()

    print "These are your hashtags: \n ", data_point.get_hashtags()
    print "These are your lowercase hashtags: \n ", data_point.get_lowercase_hashtags()

#### TODO: printing the matching pos/neg words in hashtags shows that e.g. suck and sucks are found.
#### That's not cool, because they correspond to the same word in the hashtag.
#### If only the longer one is counted then: in "#suckyweather #lifesucks" only one of them
#### will be found, when it's two bad words. But if we keep counting both, we count twice
#### the same word as in the example below... Sooo... Needs some fix
    print "Number of positive words in hashtags: \n ", data_point.count_positive_words_in_hashtags()
    print "Number of negative words in hashtags: \n ", data_point.count_negative_words_in_hashtags()


    print "This is your data tagged in a misterious way: \n ", data_point.pos_tag_data_string()
    print "Number of adjectives (JJ): ", data_point.count_adjectives()
    # Example for counting more than one part of speech:
    print "Number of adjectives (JJ) and adverbs (RB): ", data_point.count_multiple_types_in_tags(['JJ', 'RB'])
    '''

