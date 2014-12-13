import os
import cPickle
import numpy as np
from TSVParser import TSV_Getter
from TrainingData import TrainingData, get_normalized_feature_dictionary
from DataPoint import DataPoint
import numpy.random as npr

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


def load_feat_matrix(data_map, max_amount_data_per_class=None, selected_features=None):
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
                       TSV_Getter(file_path).get_all_tsv_objects(max_amount_data_per_class)]

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
    def __init__(self, data_class, n, training_percentage, selected_features=None, is_bootstrap=True):
        self.data_class = data_class
        self.n_per_class = n
        self.training_percentage = training_percentage

        if selected_features is None:
            self.selected_features = feature_dictionary
        else:
            self.selected_features = selected_features

        self.is_bootstrap = is_bootstrap

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
        data_length = []

        print('Feature extraction...')

        print('== reading source files:')
        for c in self.data_class:
            source_data = TSV_Getter(c[0]).get_all_tsv_objects()
            idx_start = len(data_points)
            data_points = data_points + [DataPoint(_.text, _.hashtags, c[1]) for _ in source_data]
            idx_end = len(data_points)
            data_length.insert(c[1], [idx_start, idx_end, len(source_data)])

        # Randomize indices
        # if data is not balanced we can do bootstrapping (samples with replacement)
        if self.is_bootstrap is True and self.n_per_class is not None:
            # print data_length

            train_indices = np.array([])
            test_indices = np.array([])
            for d in data_length:
                idx_min = d[0]
                idx_max = d[1] - 1

                train_size = (1, np.floor(self.n_per_class * self.training_percentage))
                train_indices = np.append(train_indices, npr.randint(idx_min, idx_max, size=train_size))

                test_size = (1, self.n_per_class - np.floor(self.n_per_class * self.training_percentage))
                test_indices = np.append(test_indices, npr.randint(idx_min, idx_max, size=test_size))
                # print idx_min, idx_max, train_size, test_size

            train_indices = train_indices.flatten().astype(int)
            test_indices = test_indices.flatten().astype(int)

        else:
            train_indices = np.array([])
            test_indices = np.array([])
            for d in data_length:
                idx_min = d[0]
                idx_max = d[1] - 1
                idx_len = d[2]

                # min file or self.n_per_class * self.training_percentage
                _size = np.floor(self.n_per_class * self.training_percentage)
                train_size = (1, np.min(_size, idx_len))
                train_indices = np.append(train_indices, npr.randint(idx_min, idx_max, size=train_size))

                _size = self.n_per_class - _size
                test_size = (1, np.min(_size, idx_len))
                test_indices = np.append(test_indices, npr.randint(idx_min, idx_max, size=test_size))
                # print idx_min, idx_max, train_size, test_size

            train_indices = train_indices.flatten().astype(int)
            test_indices = test_indices.flatten().astype(int)

            # size_all = len(data_points)
            # indices = list(range(size_all))  # if data is balanced (hopefully)
            # n_train = np.floor(size_all * self.training_percentage).astype(int)
            # train_indices = random.sample(indices, n_train)
            # test_indices = [index for index in indices if index not in train_indices]

        # feature matrix
        print('== check caches data:')
        feat_matrix = load_feat_matrix(self.data_class, None, self.selected_features)

        # Divide the data into train and test data
        # Get the feature matrix of this data
        training_data = TrainingData([data_points[i] for i in train_indices])
        training_label = training_data.get_label_vector()
        training_feature_matrix = np.array([feat_matrix[i] for i in train_indices])

        test_data = TrainingData([data_points[i] for i in test_indices])
        test_label = test_data.get_label_vector()
        test_feature_matrix = np.array([feat_matrix[i] for i in test_indices])

        return training_data, \
               training_feature_matrix, \
               training_label, \
               test_data, \
               test_feature_matrix, \
               test_label


class GetDataUbuntu():
    def __init__(self, filenames, selected_features=None):
        self.filenames = filenames
        # self.training_percentage = training_percentage

        if selected_features is None:
            self.selected_features = feature_dictionary
        else:
            self.selected_features = selected_features

        self.data_features, \
        self.data_features_per_user, \
        self.data_labels_per_user = self.get_data_features()

    def get_labels_per_user(self):
        return self.data_labels_per_user

    def get_feature_matrix(self):
        return self.data_features

    def get_feature_matrix_per_user(self):
        return self.data_features_per_user

    def get_data_features(self):
        data_points = []
        data_labels_per_user = []
        combined_feat_dict = {}

        # read and extract feature
        for file_path in self.filenames:

            # use cache file to fetch/store extracted feature from file
            filename = file_path + '.__feat_matrix__.cache'

            if os.path.isfile(filename) and os.access(filename, os.R_OK):
                fh = open(filename, "rb")

                # load cache file
                structure, feature_dict, data_labels_per_user = cPickle.load(fh)
                fh.close()

            else:
                fh = open(filename, "wb")

                source_data = TSV_Getter(file_path).get_sorted_tsv_objects()
                structure = []

                for username in source_data:
                    user_messages = []
                    user_labels = []

                    for message in username:
                        user_messages.append(DataPoint(message.get_text(), message.get_tags(), message.get_label()))
                        user_labels.append(message.get_label());

                    data_points += user_messages
                    structure.append(len(username))
                    data_labels_per_user.append(user_labels);

                # extract feature (everything.. we surely will hand-pick them later, but for the sake of caching, do it all)
                feature_dict = TrainingData(data_points).get_unnormalize_feature_matrix()

                # store to cache file
                cPickle.dump([structure, feature_dict, data_labels_per_user], fh)
                fh.close()

            # aggregate them
            # combined_feat_matrix = feature_matrix
            for feature in self.selected_features:
                # of course we should check if it exists
                if combined_feat_dict.has_key(feature):
                    combined_feat_dict[feature] += feature_dict[feature]
                else:
                    combined_feat_dict[feature] = feature_dict[feature]

        # normalized feature matrix
        normalized_feature_dictionary = get_normalized_feature_dictionary(combined_feat_dict)

        index = 0
        feat_matrix_all = []
        feat_matrix = []
        labels_per_user = []

        for n_messages in structure:
            feat_matrix_per_user = []

            for i in xrange(0, n_messages):
                temp = [d[index] for d in normalized_feature_dictionary.values()]
                feat_matrix_per_user.append(temp)
                index += 1

            feat_matrix.append(feat_matrix_per_user)
            feat_matrix_all += feat_matrix_per_user

        for user_labels in data_labels_per_user:
            parsed_labels = []

            for label in user_labels:
                parsed_label = label[1:-1]
                parsed_labels.append(parsed_label)

            labels_per_user.append(parsed_labels)

        return feat_matrix_all, feat_matrix, labels_per_user


if __name__ == "__main__":
    n_per_class = 5
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        # ['../Data/Twitter/hc2', 1, ';D'],
        # ['../Data/Twitter/hc3', 2, ';)'],
        # ['../Data/Twitter/hc4', 3, ';-D'],
        # ['../Data/Twitter/hc5', 4, ';-P'],
        # ['../Data/Twitter/hc6', 5, ';P'],
        ['../Data/Twitter/hc7', 6, ';-('],
        # ['../Data/Twitter/hc8', 7, ';('],
        # ['../Data/Twitter/hc9', 8, ';o'],
        # ['../Data/Twitter/hc10', 9, ';]'],
        # ['../Data/Twitter/hc11', 10, '=]'],
        # ['../Data/Twitter/hc13', 11, ';*'],
        # ['../Data/Twitter/hc15', 12, ';|'],
        # ['../Data/Twitter/hc_non', 13, '_non_'],
    ]

    # data_class = [
    # ['2006-05-27-#ubuntu-negative.tsv', ':('],
    # ['2006-05-27-#ubuntu-positive.tsv', ':)']
    # ]

    # load data from tsv and build data collection
    selected_features = [
        "words",
        "negative_words",
        "positive_words",
        # "positive_words_hashtags",
        # "negative_words_hashtags",
        # "uppercase_words",
        # "special_punctuation",
        # "adjectives"
    ]

    training_percentage = 0.9

    filenames = [
        "../Data/Chat Data/2006-05-27-#ubuntu.tsv",
        # "../Data/Chat Data/2006-06-01-#ubuntu.tsv",
        # "../Data/Chat Data/2007-04-20-#ubuntu.tsv",
        # "../Data/Chat Data/2007-04-21-#ubuntu.tsv",
        # "../Data/Chat Data/2007-04-22-#ubuntu.tsv",
        # "../Data/Chat Data/2007-10-19-#ubuntu.tsv",
        # "../Data/Chat Data/2007-10-20-#ubuntu.tsv",
        # "../Data/Chat Data/2007-10-21-#ubuntu.tsv",
        # "../Data/Chat Data/2008-04-25-#ubuntu.tsv",
        # "../Data/Chat Data/2008-04-26-#ubuntu.tsv",
    ]

    dataCollection = GetDataUbuntu(filenames, selected_features)
    feat_mat = dataCollection.get_feature_matrix()
    feat_mat_user = dataCollection.get_feature_matrix_per_user()
    print feat_mat
    print feat_mat_user
