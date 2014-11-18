from TSVParser import TSV_Getter
from TrainingData import TrainingData
from DataPoint import DataPoint
from Dictionary import Dictionary

class GetData:
    def __init__(self, data_class, n, training_percentage):
        self.data_class = data_class
        self.n_per_class = n
        self.training_percentage = training_percentage
        self.dictionary = Dictionary()

        raw_training, raw_test = self.load_tsv()
        self.training_data, self.training_label = self.create_data_and_label(raw_training)
        self.test_data, self.test_label = self.create_data_and_label(raw_test)

    def get_training_data(self):
        return self.training_data

    def get_training_label(self):
        return self.training_label

    def get_test_data(self):
        return self.test_data

    def get_test_label(self):
        return self.test_label


    # Helper functions
    def load_tsv(self):
        training = []
        test = []

        for index, cls in enumerate(self.data_class):
            temp = TSV_Getter(cls[0]).get_all_tsv_objects(self.n_per_class)

            length = len(temp)
            training_length = int(round(self.training_percentage * length))

            training.append(temp[0:training_length])
            test.append(temp[training_length:length])

        return training, test

    def create_data_and_label(self, raw_data):
        data = []
        labels = []
        length = len(raw_data[0])

        for i in range(0, length):
            for j in range(0, len(self.data_class)):
                raw_data_point = raw_data[j][i]
                label = self.data_class[j][1]

                data_point = DataPoint(raw_data_point.text, raw_data_point.hashtags, label, self.dictionary)

                data.append(data_point)
                labels.append(label)

        return TrainingData(data), labels


