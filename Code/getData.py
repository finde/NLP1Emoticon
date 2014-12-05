import os
import cPickle
import numpy as np
from TSVParser import TSV_Getter
from TrainingData import TrainingData, get_normalized_feature_dictionary
from DataPoint import DataPoint

import random

feature_dictionary = [
    "words",
    "negative_words",
    "positive_words",
    "positive_words_hashtags",
    "negative_words_hashtags",
    "uppercase_words",
    "special_punctuation",
    "adjectives"
]


def load_feat_matrix(data_map, amount_data_per_class=None, selected_features=None):
    # todo: support ubuntu chat data as well

    """
    to load feature matrix from cache file to extract them with TrainingData class
    :param data_map: list of files and the label (for twitter)
    :param amount_data_per_class:
    :param selected_features:
    :return:
    """
    data_points = []
    combined_feat_matrix = {}

    n_data = 0

    if selected_features is None:
        selected_features = feature_dictionary

    # read and extract feature
    for c in data_map:
        file_path = c[0]
        label = c[1]
        data_points = [DataPoint(_.text, _.hashtags, label) for _ in
                       TSV_Getter(file_path).get_all_tsv_objects(amount_data_per_class)]

        n_data += len(data_points)

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
            if combined_feat_matrix.has_key(feature):
                combined_feat_matrix[feature] += unnormalized_feature_matrix[feature]
            else:
                combined_feat_matrix[feature] = unnormalized_feature_matrix[feature]

    # normalized feature matrix
    normalized_feature_dictionary = get_normalized_feature_dictionary(combined_feat_matrix)
    feat_matrix = [[d[i] for d in normalized_feature_dictionary.values()] for i in range(0, n_data)]

    return feat_matrix


class GetData:
    def __init__(self, data_class, n, training_percentage, selected_features=None):
        self.data_class = data_class
        self.n_per_class = n
        self.training_percentage = training_percentage

        if selected_features is None:
            self.selected_features = feature_dictionary
        else:
            self.selected_features = selected_features

        # all_data = self.load_tsv()
        self.training_data, \
        self.training_feature_matrix, \
        self.training_label, \
        self.test_data, \
        self.test_feature_matrix, \
        self.test_label = self.split_training_and_test()

    def get_training_data(self):
        return self.training_data

    def get_training_label(self):
        return self.training_label

    def get_training_feature_matrix(self):
        return self.training_feature_matrix

    def get_test_data(self):
        return self.test_data

    def get_test_label(self):
        return self.test_label

    def get_test_feature_matrix(self):
        return self.test_feature_matrix

    def split_training_and_test(self):
        data_points = []

        print('Feature extraction...')

        print('== reading source files:')
        for c in self.data_class:
            data_points = data_points + [DataPoint(_.text, _.hashtags, c[1]) for _ in
                                         TSV_Getter(c[0]).get_all_tsv_objects(self.n_per_class)]

        # gather the data points into a whole training data
        all_data = TrainingData(data_points)

        # You can print the data if you wanna see it
        # training_data.print_data()

        # Show the features
        # print training_data.get_feature_dictionary()
        # print training_data.get_label_vector()

        # Randomize indices
        size_all = len(data_points)

        indices = list(range(size_all))
        n_train = np.floor(size_all * self.training_percentage).astype(int)
        random_indices = random.sample(indices, n_train)
        rest_indices = [index for index in indices if index not in random_indices]

        # feature matrix
        print('== check caches data:')
        feat_matrix = load_feat_matrix(self.data_class, self.n_per_class, self.selected_features)

        # Divide the data into train and test data (do it in a smarter way in the feature :D)
        # Get the feature matrix of this data
        training_data = TrainingData([data_points[i] for i in random_indices])
        training_label = training_data.get_label_vector()
        training_feature_matrix = np.array([feat_matrix[i] for i in random_indices])

        test_data = TrainingData([data_points[i] for i in rest_indices])
        test_label = test_data.get_label_vector()
        test_feature_matrix = np.array([feat_matrix[i] for i in rest_indices])

        return training_data, \
               training_feature_matrix, \
               training_label, \
               test_data, \
               test_feature_matrix, \
               test_label