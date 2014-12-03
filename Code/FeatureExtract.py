from __future__ import division

from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint
import cPickle
import ntpath
import os
import numpy as np

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

    data_points = []
    amount_data_per_class = 300

    combined_feat_matrix = {}

    # read and extract feature
    for c in data_class:
        # comment line below for balanced data source
        # amount_data_per_class = None
        data_points = [DataPoint(_.text, _.hashtags, c[1]) for _ in
                       TSV_Getter(c[0]).get_all_tsv_objects(amount_data_per_class)]


        # use cache file
        filename = '../Data/Twitter/cache.__feat_matrix__.' + ntpath.basename(c[0]) + '.p'
        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            fh = open(filename, "rb")
            feat_matrix = cPickle.load(fh)
            fh.close()
        else:
            fh = open(filename, "wb")
            feat_matrix = TrainingData(data_points).get_unnormalize_feature_matrix()
            cPickle.dump(feat_matrix, fh)
            fh.close()

            # print filename

    # add to the feat_matrix
    normalized_feature_dict = {}

    for feature in combined_feat_matrix:
        feature_values = combined_feat_matrix[feature]

        max_value = max(feature_values)
        min_value = min(feature_values)

        denominator = max_value - min_value
        denominator = 1 if denominator == 0 else denominator

        normalized_values = []

        for value in feature_values:
            normalized_value = ((0.9 - 0.1) * (value - min_value) / denominator) + 0.1
            normalized_values.append(normalized_value)

        normalized_feature_dict[feature] = normalized_values

    print normalized_feature_dict