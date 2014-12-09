import os
import numpy as np
import random
from TrainingData import TrainingData
from DataPoint import DataPoint
from TSVParser import TSV_Getter
import cPickle
from getData import GetData


def mlp_gradient(x, t, w, b, v, a, L, number_classes, number_features):
    # initialize datastructures w, b, v and a to fill later on
    gradW = np.zeros((L, number_classes))
    gradB = np.zeros(number_classes)
    gradV = np.zeros((number_features, L))
    gradA = np.zeros(L)

    # print x
    # calculate h
    h = 1 / (1 + np.exp(-(v.T.dot(x) + a)))

    # calculate gradient for w and b as usual, only logQ is a bit different than before, so the result will be different.
    logQ = (w.T.dot(h)).T + b
    c = logQ.max()
    qc = np.exp(logQ - c)
    logZ = c + np.log(sum(qc))

    # store derivatives
    for j in range(0, number_classes):
        gradB[j] = ((j == t) - np.exp(logQ[j] - logZ))
        gradW[:, j] = h * gradB[j]


    # compute deltaH and compute gradients
    deltaH = w.dot(gradB)
    gradA = deltaH.T * h * (1 - h)
    gradV = np.outer(x, (deltaH.T * h * (1 - h)))

    # return gradients
    return gradW, gradB, gradA, gradV


def mlp_iter(x_train, t_train, w, b, v, a, L, number_classes, number_features):
    # create a number of indices
    r = list(range(x_train.shape[0]))

    # shuffle numbers in r to iterate over our trainingset in a random way
    np.random.shuffle(r)
    for row in r:
        gradW, gradB, gradA, gradV = mlp_gradient(x_train[row, :], t_train[row], w, b, v, a, L, number_classes,
                                                  number_features)

        # update gradients, but multiply by small learning rate to keep the weights small
        learning_rate = 1E-3
        w += gradW * learning_rate
        b += gradB * learning_rate
        v += gradV * learning_rate
        a += gradA * learning_rate
    return w, b, v, a


def mlp_train_set(w, b, v, a, N, L, x_train, t_train, number_classes, number_features):
    for i in range(0, N):
        print 'interation :', i + 1
        w, b, v, a = mlp_iter(x_train, t_train, w, b, v, a, L, number_classes, number_features);
    return w, b, v, a


def mlp_predict(w, b, v, a, x_test, t_test, data_class):
    h = 1 / (1 + np.exp(-(x_test.dot(v) + a)))

    # implement the gradients we derived
    logQ = (h.dot(w)) + b
    q = np.exp(logQ)
    Z = sum(q)

    c = logQ.max()
    qc = np.exp(logQ - c)
    logZ = c + np.log(sum(qc))

    logP = logQ - logZ

    cnt = 0

    predicted_labels = []
    # count number of correctly labeled images
    for i in range(t_test.shape[0]):
        classification = np.argmax(logP[i, :])
        # TODO: These probabilities seem weird, find out if that's expected behaviour

        # classification is a label's index
        # we need to translate it back to the actual label
        predicted_label = data_class[classification][1]
        predicted_labels.append(data_class[classification][2])

        # print predicted_label, t_test[i], np.exp(logP[i, :]), ' '
        if predicted_label == t_test[i]:
            cnt += 1
    return cnt, t_test.shape[0], predicted_labels


def cluster_to_3_classes(string_label):
    for i in [0, 1, 2, 3, 4, 5, 9, 10, 11]:
        if i == string_label:
            return 'happy'

    for i in [6, 7]:
        if i == string_label:
            return 'sad'

    for i in [8, 12, 13]:
        if i == string_label:
            return 'neutral'

    return 'neutral'


if __name__ == "__main__":
    n_per_class = 1000  # data sample per class
    training_percentage = 0.9  # train-test percentage
    N = 100  # iteration
    L = 5  # hidden layer

    '''
    # Reading
    '''

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
        ['../Data/Twitter/hc_non', 13, '_non_'],
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
        "special_punctuation",
        "adjectives"
    ]

    dataCollection = GetData(data_class, n_per_class, training_percentage, selected_features)

    # split data collection into training and test data
    training_data = dataCollection.get_training_data()
    training_label = np.array(dataCollection.get_training_label())
    test_data = dataCollection.get_test_data()
    test_label = np.array(dataCollection.get_test_label())

    print('Extracting features...')

    # Get the feature matrix of this data
    print(' extracting train_data')
    training_features = dataCollection.get_training_feature_matrix()

    print(' extracting test_data')
    test_features = dataCollection.get_test_feature_matrix()

    # These are the parameters - #of features in the hidden layer, #of iterations to perform and #of classes and features
    number_classes = len(data_class)
    number_features = len(selected_features)

    # start with really small initial weights!!
    w = np.random.randn(L, number_classes) * 0.15
    b = np.random.randn(number_classes) * 0.015
    v = np.random.randn(number_features, L) * 0.15
    a = np.random.randn(L) * 0.015

    # print 'WWWWWWWWWWWWWWWWWW', w
    print 'Learning... , samples:', training_label.shape[0]

    # So we learn the parameters
    w, b, v, a = mlp_train_set(w, b, v, a, N, L, training_features, training_label, number_classes, number_features)

    # print 'WWWWWWWWWWWWWWWWWW', w
    print 'Predict...'

    '''
    # Predicting
    '''

    # And then we use them to test
    count_correct, count_total, _ = mlp_predict(w, b, v, a, training_features, training_label, data_class)
    # print '  cnt: ', count_correct
    # print '  cntall: ', count_total
    print '  train accuracy: ', 1.0 * count_correct / count_total * 100, '%'

    count_correct, count_total, _ = mlp_predict(w, b, v, a, test_features, test_label, data_class)
    print '  test accuracy: ', 1.0 * count_correct / count_total * 100, '%'

    # ### new Data ####
    # new_data_point = [
    #     DataPoint(
    #         "yes i like the new edubuntu background too - although it's a kinda cold and is missing New Zealand (bug reported)",
    #         [], '?'),
    #     DataPoint('super, mega, definitely not', [], '?')
    # ]
    # new_data_feat = TrainingData(new_data_point).get_feature_matrix()
    # _, _, predicted_label = mlp_predict(w, b, v, a, np.array(new_data_feat), np.array(xrange(0, len(new_data_point))),
    #                                     data_class)
    # print predicted_label

'''
Just saving some weights here for test purposes :P 
0015 and 015
WWWWWWWWWWWWWWWWWW [[ 0.03680083 -0.01718052]
 [ 0.01356237  0.0149547 ]
 [ 0.00702975 -0.00297079]]
WWWWWWWWWWWWWWWWWW [[-0.70942263  0.72904294]
 [-0.25232536  0.28084243]
 [-0.36663171  0.37069068]]
 
0025 and 025
 WWWWWWWWWWWWWWWWWW [[-0.00974345  0.0010707 ]
 [-0.00587517  0.00974238]
 [-0.02237335  0.03998623]]
WWWWWWWWWWWWWWWWWW [[-0.63406381  0.62539106]
 [ 0.21843463 -0.21456742]
 [-0.90502857  0.92264145]]
 
025 and 25
WWWWWWWWWWWWWWWWWW [[-0.19491818 -0.20358173]
 [ 0.01205856  0.12002121]
 [-0.15401177 -0.25199409]]
WWWWWWWWWWWWWWWWWW [[ 0.65981482 -1.05831473]
 [ 0.54044648 -0.4083667 ]
 [-1.11662407  0.7106182 ]]
 
 WWWWWWWWWWWWWWWWWW [[ 0.04358235  0.02683832]
 [-0.20655984 -0.14810111]
 [ 0.11560181  0.28404154]]
WWWWWWWWWWWWWWWWWW [[ 0.40703629 -0.33661561]
 [-1.18129089  0.82662993]
 [ 0.84203249 -0.44238913]]


'''