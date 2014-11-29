from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint
from Dictionary import Dictionary

import random

class GetData:
    def __init__(self, data_class, n, training_percentage):
        self.data_class = data_class
        self.n_per_class = n
        self.training_percentage = training_percentage
        self.dictionary = Dictionary()

        all_data = self.load_tsv()
        self.training_data, self.training_label, self.test_data, self.test_label = self.split_training_and_test(all_data)

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

            raw = TSV_Getter(filename).get_all_tsv_objects(None)

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

                data_point = DataPoint(current.get_text(), current.get_tags(), class_label, self.dictionary)
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
