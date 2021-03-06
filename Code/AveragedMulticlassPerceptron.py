import collections
from getData import GetData
from TrainingData import TrainingData
from DataPoint import DataPoint

NULL_LABEL = '__NULL_LABEL__'


def score(features, weights):
    return sum(weights.get(f, 0) for f in features)


# based on https://github.com/lmjohns3/py-perceptron
class Multiclass:
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
    all_trains = []
    all_tests = []
    n_per_class = 300  # number of data points per each class
    training_percentage = 0.8  # percentage of training data from all data
    iteration = 50
    nr_of_tests = 10

    for ex in range(0,nr_of_tests):
	    print('Reading data...')

	    # Define data per class
	    data_class = [
		['../Data/Twitter/hc1', 0, ';-)'],
		['../Data/Twitter/hc2', 0, ';-)'],
		['../Data/Twitter/hc3', 0, ';-)'],
		['../Data/Twitter/hc4', 0, ';-)'],
		['../Data/Twitter/hc5', 0, ';-)'],
		['../Data/Twitter/hc6', 0, ';-)'],
		['../Data/Twitter/hc7', 1, ';-('],
		['../Data/Twitter/hc8', 1, ';-('],
#		['../Data/Twitter/hc9', 2, ';o'],
		['../Data/Twitter/hc10', 0, ';-)'],
		['../Data/Twitter/hc11', 0, ';-)'],
		['../Data/Twitter/hc13', 0, ';-)'],
#		['../Data/Twitter/hc15', 2, ';|'],
#		['../Data/Twitter/hc_non', 2, '_non_'],
		['../Data/Twitter/negative_tabed.tsv', 0, ';-)'],
		['../Data/Twitter/positive_tabed.tsv', 1, ';-('],
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
#		"positive_words_hashtags",
#		"negative_words_hashtags",
		"uppercase_words",
		"special_punctuation",
		"adjectives"
	    ]

	    dataCollection = GetData(data_class, n_per_class, training_percentage, selected_features=selected_features)

	    # split data collection into training and test data
	    training_data = dataCollection.get_training_data()
	    training_label = dataCollection.get_training_label()
	    test_data = dataCollection.get_test_data()
	    test_label = dataCollection.get_test_label()

	    print('Extracting features...')

	    # Get the feature matrix of this data
	    print(' extracting train_data')
	    training_features = dataCollection.get_training_feature_matrix()

	    print(' extracting test_data')
	    test_features = dataCollection.get_test_feature_matrix()

	    # initialize multiclass perceptron
	    multiclass = Multiclass()

	    # training perceptron
	    print 'Training perceptron... , samples:', len(training_label)

	    for n in xrange(iteration):
		print '== Iteration:', n + 1
		for i in xrange(len(training_data.data_points)):
		    multiclass.learn(training_features[i], training_label[i])

	    print('Predicting...')
	    # accuracy for training data
	    count = 0
	    for i in xrange(len(training_data.data_points)):
		predicted_class = multiclass.predict(training_features[i])

		print "train: ", training_label[i], " prediction: ", predicted_class
		if training_label[i] == predicted_class:
		    count += 1

	    train_acc = count * 100.0 / len(training_label)
	    print "  training accuracy = ", train_acc, '%'
	    all_trains.append(train_acc)
	    # accuracy for test data
	    count = 0
	    for i in xrange(len(test_data.data_points)):
		predicted_class = multiclass.predict(test_features[i])

		if test_label[i] == predicted_class:
		    count += 1
	    test_acc = count * 100.0 / len(test_label)
	    print "  test accuracy = ", test_acc, '%'
	    all_tests.append(test_acc)

	    # todo: store w and config
	    # ###### NEW test #######
	    # new_data_point = [
	    # DataPoint('Yippiee holiday is coming, I am so happy', [], '?'),
	    #     DataPoint('Buu huuu.... I am lost... sad', [], '?')
	    # ]
	    # new_data_feat = TrainingData(new_data_point).get_feature_matrix()
	    # for i in new_data_feat:
	    #     print multiclass.predict(i)
    print "averaged over runs: ", nr_of_tests
    print "datapoints per class: ", n_per_class
    print "training percentage: ", training_percentage
    print "iterations: ", iteration
    print "features: ", selected_features
    print "train accuracies: ", all_trains
    print "average train accuracy: ", sum(all_trains)/len(all_trains)
    print "test accuracies: ", all_tests
    print "average test accuracy: ", sum(all_tests)/len(all_tests)
