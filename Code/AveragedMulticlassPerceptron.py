import collections
import progressbar
from getData import GetData
import time

NULL_LABEL = '__NULL_LABEL__'


def score(features, weights):
    return sum(weights.get(f, 0) for f in features)


class Perceptron:
    def __init__(self):
        self.weights = collections.defaultdict(float)
        self.edges = collections.defaultdict(float)
        self.count = 0

    def learn(self, features, label):
        if self.predict(features) ^ bool(label):
            for f in features:
                self.edges[f] += 1
        self.average()

    def predict(self, features):
        return score(features, self.weights) > 0

    def average(self):
        c = self.count
        for f, w in self.edges.iteritems():
            self.weights[f] = (c * self.weights[f] + w) / (c + 1)
        self.count += 1


class Multiclass(Perceptron):
    def __init__(self):
        self.weights = collections.defaultdict(
            lambda: collections.defaultdict(float))
        self.edges = collections.defaultdict(
            lambda: collections.defaultdict(float))
        self.count = 0

    def learn(self, features, label):
        toward = self.edges[label]
        predicted = self.predict(features, True)
        if predicted is NULL_LABEL:
            for f in features:
                toward[f] += 1
        elif predicted != label:
            away = self.edges[predicted]
            for f in features:
                toward[f] += 1
                away[f] -= 1
        self.average()

    def predict(self, features, edge=False):
        sources = self.weights
        if edge:
            sources = self.edges
        if not sources:
            return NULL_LABEL
        return max((score(features, ws), l) for l, ws in sources.iteritems())[1]

    def average(self):
        c = self.count
        for l, sources in self.edges.iteritems():
            targets = self.weights[l]
            for f, w in sources.iteritems():
                targets[f] = (c * targets[f] + w) / (c + 1)
        self.count += 1


if __name__ == "__main__":

    n_per_class = 200  # number of data points per each class
    training_percentage = 0.75  # percentage of training data from all data

    print('Reading data...')
    # Define data per class
    # data_class = [
    # ['negative.tsv', ':('],
    # ['positive.tsv', ':)']
    # ]

    n_per_class = None
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        ['../Data/Twitter/hc2', 1, ';D'],
        # ['../Data/Twitter/hc3', 2, ';)'],
        # ['../Data/Twitter/hc4', 3, ';-D'],
        # ['../Data/Twitter/hc5', 4, ';-P'],
        # ['../Data/Twitter/hc6', 5, ';P'],
        # ['../Data/Twitter/hc7', 6, ';-('],
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
    dataCollection = GetData(data_class, n_per_class, training_percentage)

    # split data collection into training and test data
    training_data = dataCollection.get_training_data()
    training_label = dataCollection.get_training_label()
    test_data = dataCollection.get_test_data()
    test_label = dataCollection.get_test_label()

    print('Extracting features...')

    # Get the feature matrix of this data
    print(' extracting train_data')
    training_features = training_data.get_feature_matrix()

    print(' extracting test_data')
    test_features = test_data.get_feature_matrix()

    # initialize multiclass perceptron
    multiclass = Multiclass()

    # training perceptron
    iteration = 50
    print 'Training perceptron... ', iteration, 'times'
    time.sleep(1)
    bar = progressbar.ProgressBar(maxval=iteration,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    for n in xrange(iteration):
        bar.update(n)
        for i in xrange(len(training_data.data_points)):
            multiclass.learn(training_features[i], training_label[i])
    bar.finish()
    time.sleep(1)

    print('Predicting...')
    # accuration for training data
    count = 0
    for i in xrange(len(training_data.data_points)):
        predicted_class = multiclass.predict(training_features[i])
        if training_label[i] == predicted_class:
            count += 1

    print "  training accuracy = ", count * 100.0 / len(training_label), '%'

    # accuration for test data
    count = 0
    for i in xrange(len(test_data.data_points)):
        predicted_class = multiclass.predict(test_features[i])
        if test_label[i] == predicted_class:
            count += 1

    print "  test accuracy = ", count * 100.0 / len(test_label), '%'
