from __future__ import division

from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint
import cPickle
import ntpath
import os
import numpy as np
from TrainingData import get_normalized_feature_dictionary

# todo: support ubuntu chat data as well
def load_feat_matrix(data_map, amount_data_per_class=None, selected_features=["words"]):
    """
    to load feature matrix from cache file to extract them with TrainingData class
    :param data_map: list of files and the label (for twitter)
    :param amount_data_per_class:
    :param selected_features:
    :return:
    """
    data_points = []
    combined_feat_matrix = {}

    # read and extract feature
    for c in data_map:
        file_path = c[0]
        label = c[1]
        data_points = [DataPoint(_.text, _.hashtags, label) for _ in
                       TSV_Getter(file_path).get_all_tsv_objects(amount_data_per_class)]

        data_size = len(data_points)

        # use cache file to fetch/store extracted feature from file
        filename = file_path + '.__feat_matrix__.cache'
        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            fh = open(filename, "rb")

            # load cache file
            unnormalized_feature_matrix = cPickle.load(fh)
            fh.close()

        else:
            fh = open(filename, "wb")

            # extract feature (everything.. we surely will hand-pick them later, but for the sake of caching, do it all)
            unnormalized_feature_matrix = TrainingData(data_points).get_unnormalize_feature_matrix()

            # store to cache file
            cPickle.dump(unnormalized_feature_matrix, fh)
            fh.close()

        # aggregate them
        # combined_feat_matrix = unnormalized_feature_matrix
        for feature in selected_features:
            # of course we should check if it exists
            if hasattr(combined_feat_matrix, feature):
                combined_feat_matrix[feature] += unnormalized_feature_matrix[feature]
            else:
                combined_feat_matrix[feature] = unnormalized_feature_matrix[feature]

    # normalized feature matrix
    normalized_feature_dictionary = get_normalized_feature_dictionary(combined_feat_matrix)
    feat_matrix = [[d[i] for d in normalized_feature_dictionary.values()] for i in range(0, data_size)]

    return feat_matrix


feature_dictionary = {"words": 1,
                      "negative_words": 2,
                      "positive_words": 3,
                      "positive_words_hashtags": 4,
                      "negative_words_hashtags": 5,
                      "uppercase_words": 6,
                      "special_punctuation": 7,
                      "adjectives": 8}

if __name__ == "__main__":
    # load file
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        ['../Data/Twitter/hc2', 1, ';D'],
        ['../Data/Twitter/hc3', 2, ';)'],
        ['../Data/Twitter/hc4', 3, ';-D'],
        ['../Data/Twitter/hc5', 4, ';-P'],
        ['../Data/Twitter/hc6', 5, ';P'],
        ['../Data/Twitter/hc7', 6, ';-('],
        ['../Data/Twitter/hc8', 7, ';('],
        ['../Data/Twitter/hc9', 8, ';o'],
        ['../Data/Twitter/hc10', 9, ';]'],
        ['../Data/Twitter/hc11', 10, '=]'],
        ['../Data/Twitter/hc13', 11, ';*'],
        ['../Data/Twitter/hc15', 12, ';|'],
        ['../Data/Twitter/hc_non', 13, '_non_']
    ]

    selected_feature = [
        "words",
        "negative_words",
        "positive_words",
        # "positive_words_hashtags",
        # "negative_words_hashtags",
        # "uppercase_words",
        # "special_punctuation",
        # "adjectives"
    ]

    print load_feat_matrix(data_class, None, selected_feature)


