from __future__ import division

from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint
import cPickle
import ntpath
import os
import numpy as np
from TrainingData import get_normalized_feature_dictionary


def load_feat_matrix(data_class, amount_data_per_class=None):
    data_points = []
    combined_feat_matrix = {}

    # read and extract feature
    for c in data_class:
        data_points = [DataPoint(_.text, _.hashtags, c[1]) for _ in
                       TSV_Getter(c[0]).get_all_tsv_objects(amount_data_per_class)]


        # use cache file to fetch/store extracted feature from file
        filename = '../Data/Twitter/cache.__feat_matrix__.' + ntpath.basename(c[0]) + '.p'
        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            fh = open(filename, "rb")

            # load cache file
            unnormalized_feature_matrix = cPickle.load(fh)
            fh.close()

        else:
            fh = open(filename, "wb")

            # extract feature
            unnormalized_feature_matrix = TrainingData(data_points).get_unnormalize_feature_matrix()

            # store to cache file
            cPickle.dump(unnormalized_feature_matrix, fh)
            fh.close()

        # aggregate them
        if len(combined_feat_matrix) == 0:
            combined_feat_matrix = unnormalized_feature_matrix
        else:
            # combined_feat_matrix = unnormalized_feature_matrix
            for index, feature in enumerate(unnormalized_feature_matrix):
                combined_feat_matrix[feature] += unnormalized_feature_matrix[feature]
                # combined_feat_matrix +=
                # todo: for each selected feature
                # todo: append feat_matrix to the feature_dictionary

    # normalized feature matrix
    normalized_feature_dictionary = get_normalized_feature_dictionary(combined_feat_matrix)
    feat_matrix = [[d[i] for d in normalized_feature_dictionary.values()] for i in
                   range(0, len(normalized_feature_dictionary['adjectives']))]

    return feat_matrix


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

    print load_feat_matrix(data_class, None)


