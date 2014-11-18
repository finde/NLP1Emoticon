import TrainingData
from Dictionary import Dictionary
import DataPoint
from TSVParser import TSV_Getter

import lmj.perceptron.averaged as AMP
from getData import GetData

if __name__ == "__main__":
    # features = [
    # [1, 1, 1],
    # [0, 0, 0],
    # [2, 2, 2]
    # ]
    #
    #
    # label = ['a', 'b', 'c']
    #

    # Generate a couple of data strings, hashtags and classes
    data_class = [
        ['negative.tsv', ':('],
        ['positive.tsv', ':)']
    ]

    n_per_class = 100 # number of data points per each class
    training_percentage = 0.75 # percentage of training data from all data

    # open the dictionaries
    # dictionary = Dictionary()

    # generate points from all the strings, hashtags, classes

    # data_points = []
    # for c in data_class:
    #     data_points = data_points + [DataPoint.DataPoint(_.text, _.hashtags, c[1], dictionary) for _ in
    #                                  TSV_Getter(c[0]).get_all_tsv_objects(50)]

    dataCollection = GetData(data_class, n_per_class, training_percentage)

    training_data = dataCollection.get_training_data()
    training_label = dataCollection.get_training_label()

    test_data = dataCollection.get_test_data()
    test_label = dataCollection.get_test_label()

    # gather the data points into a whole training data
    # training_data = TrainingData.TrainingData(data_points)

    # Get the feature matrix of this data
    training_features = training_data.get_feature_matrix()
    test_features = test_data.get_feature_matrix()



    # perceptron = Perceptron()
    # perceptron.learn(features, label)

    multiclass = AMP.Multiclass()

    for n in xrange(1000):
        for i in xrange(len(training_data.data_points)):
            multiclass.learn(training_features[i], training_label[i])

    # accuration for training data
    count = 0
    for i in xrange(len(training_data.data_points)):
        if training_label[i] == multiclass.predict(training_features[i]):
            count = count + 1

    print count * 100.0 / len(training_label)

    # accuration for test data
    count = 0
    for i in xrange(len(test_data.data_points)):
        if test_label[i] == multiclass.predict(test_features[i]):
            count = count + 1

    print count * 100.0 / len(test_label)
