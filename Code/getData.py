import os
import cPickle
import numpy as np
from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint

import random


class GetData:
    def __init__(self, data_class, n, training_percentage, data_type="twitter"):
        self.data_class = data_class
        self.n_per_class = n
        self.training_percentage = training_percentage
        self.data_type = data_type

        # all_data = self.load_tsv()
        self.training_data, \
        self.training_label, \
        self.test_data, \
        self.test_label = self.split_training_and_test_alt()

    def get_training_data(self):
        return self.training_data

    def get_training_label(self):
        return self.training_label

    def get_test_data(self):
        return self.test_data

    def get_test_label(self):
        return self.test_label


    # Helper functions
    def lin_space(self, n):
        arr = []

        for i in range(0, n):
            arr.append(i)

        return arr

    def load_tsv(self):
        raw_data = []
        data = []
        n_class = len(self.data_class)

        for index, cls in enumerate(self.data_class):
            raw_data_class = []

            filename = cls[0]
            class_label = cls[1]

            raw = TSV_Getter(filename, self.data_type).get_all_tsv_objects(None)

            arr_index = self.lin_space(len(raw))
            random.shuffle(arr_index)
            arr_index = arr_index[0:self.n_per_class]

            for idx in arr_index:
                raw_data_class.append(raw[idx])

            raw_data.append(raw_data_class)

        # reorder the data
        for i in range(0, self.n_per_class):
            for j, cls in enumerate(self.data_class):
                current = raw_data[j][i]
                class_label = cls[1]

                data_point = DataPoint(current.get_text(), current.get_tags(), class_label)
                data.append(data_point)

        return data

    def split_training_and_test(self, all_data):
        training_label = []
        test_label = []

        n_data = len(all_data)

        # make sure the number of data training always even number
        n_training = int(round(self.training_percentage * n_data))
        n_training = n_training if (n_training % 2 == 0) else (n_training - 1)

        # data training
        training_data = all_data[0:n_training]

        # data test
        test_data = all_data[n_training:n_data]

        # training label
        for data in training_data:
            training_label.append(data.get_class_label())

        # test label
        for data in test_data:
            test_label.append(data.get_class_label())

        return TrainingData(training_data), training_label, TrainingData(test_data), test_label

    # not elegant
    def split_training_and_test_alt(self):
        data_points = []

        print('Feature extraction...')

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

        # Divide the data into train and test data (do it in a smarter way in the feature :D)
        # Get the feature matrix of this data
        training_data = TrainingData([data_points[i] for i in random_indices])
        training_label = training_data.get_label_vector()

        test_data = TrainingData([data_points[i] for i in rest_indices])
        test_label = test_data.get_label_vector()

        return training_data, \
               training_label, \
               test_data, \
               test_label