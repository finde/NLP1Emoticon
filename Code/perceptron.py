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

    n_per_class = 100 # number of data points per each class
    training_percentage = 0.75 # percentage of training data from all data

    # Define data per class
    data_class = [
        ['negative.tsv', ':('],
        ['positive.tsv', ':)']
    ]

    # data_class = [
    #     ['2006-05-27-#ubuntu-negative.tsv', ':('],
    #     ['2006-05-27-#ubuntu-positive.tsv', ':)']
    # ]

    # load data from tsv and build data collection
    dataCollection = GetData(data_class, n_per_class, training_percentage)

    # split data collection into training and test data
    training_data = dataCollection.get_training_data()
    training_label = dataCollection.get_training_label()
    test_data = dataCollection.get_test_data()
    test_label = dataCollection.get_test_label()

    # Get the feature matrix of this data
    training_features = training_data.get_feature_matrix()
    test_features = test_data.get_feature_matrix()

    # initialize multiclass perceptron
    multiclass = AMP.Multiclass()

    # training perceptron
    for n in xrange(1000):
        print "iteration ", n
        for i in xrange(len(training_data.data_points)):
            multiclass.learn(training_features[i], training_label[i])

    # accuration for training data
    count = 0
    for i in xrange(len(training_data.data_points)):
        predicted_class = multiclass.predict(training_features[i])
        if training_label[i] == predicted_class:
            count = count + 1

    print "training accuration = ", count * 100.0 / len(training_label)

    # accuration for test data
    count = 0
    for i in xrange(len(test_data.data_points)):
        predicted_class = multiclass.predict(test_features[i])
        if test_label[i] == predicted_class:
            count = count + 1

    print "test accuration = ", count * 100.0 / len(test_label)
