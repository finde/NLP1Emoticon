from sklearn.linear_model import perceptron

from getData import GetData


if __name__ == "__main__":
    n_per_class = 700  # number of data points per each class
    training_percentage = 0.9  # percentage of training data from all data
    iteration = 100

    print('Reading data...')

    # Define data per class
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        ['../Data/Twitter/hc2', 0, ';D'],
        ['../Data/Twitter/hc3', 0, ';)'],
        ['../Data/Twitter/hc4', 0, ';-D'],
        ['../Data/Twitter/hc5', 0, ';-P'],
        ['../Data/Twitter/hc6', 0, ';P'],
        ['../Data/Twitter/hc7', 1, ';-('],
        ['../Data/Twitter/hc8', 1, ';('],
        ['../Data/Twitter/hc9', 2, ';o'],
        ['../Data/Twitter/hc10', 0, ';]'],
        ['../Data/Twitter/hc11', 0, '=]'],
        ['../Data/Twitter/hc13', 0, ';*'],
        ['../Data/Twitter/hc15', 2, ';|'],
        ['../Data/Twitter/hc_non', 2, '_non_'],
        ['../Data/Twitter/negative_tabed.tsv', 0, ':)'],
        ['../Data/Twitter/positive_tabed.tsv', 1, ':('],
    ]

    # load data from tsv and build data collection
    selected_features = [
        "words",
        "negative_words",
        "positive_words",
        "positive_words_hashtags",
        "negative_words_hashtags",
        "uppercase_words",
        "special_punctuation",
        "adjectives"
    ]

    dataCollection = GetData(data_class, n_per_class, training_percentage, selected_features, is_bootstrap=False)

    # split data collection into training and test data
    training_data = dataCollection.get_training_data()
    training_label = dataCollection.get_training_label()
    test_data = dataCollection.get_test_data()
    test_label = dataCollection.get_test_label()

    print('\nExtracting features..')
    training_features = dataCollection.get_training_feature_matrix()
    test_features = dataCollection.get_test_feature_matrix()

    net = perceptron.Perceptron(n_iter=iteration, verbose=1, random_state=None, shuffle=False, class_weight='auto', eta0=0.0002)

    net.fit(training_features, training_label)

    # Create the model
    print('\nPrediction..')
    # Output the values
    print "Bias " + str(net.intercept_)

    # Print the results
    print('\nTraining prediction:')
    print "Prediction " + str(net.predict(training_features))
    print "Actual     " + str(training_label)
    print "Accuracy   " + str(net.score(training_features, training_label) * 100) + "%"

    print('\nTest prediction:')
    print "Prediction " + str(net.predict(test_features))
    print "Actual     " + str(test_label)
    print "Accuracy   " + str(net.score(test_features, test_label) * 100) + "%"
