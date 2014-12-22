import os
import numpy as np
import random
import TrainingData
import DataPoint
from TSVParser import TSV_Getter
import scipy.cluster.vq as cluster
import cPickle
import Clustering
from getData import GetData
from getData import GetDataUbuntu
import pdb
from HMM import HMM
import decoding




if __name__ == "__main__":
    '''
    # Reading
    '''

    tests = 1
    avg_accuracies = []
    number_of_clusters = 50
    for i in range(0, tests):
	    selected_features = [
		"words",
		"negative_words",
		"positive_words",
		#"positive_words_hashtags",
		#"negative_words_hashtags",
		"uppercase_words",
		"special_punctuation",
		"adjectives"
	    ]

	    filenames = [
		"../Data/Chat Data/2006-05-27-#ubuntu.tsv",
		#"../Data/Chat Data/2006-06-01-#ubuntu.tsv",
		#"../Data/Chat Data/2007-04-20-#ubuntu.tsv",
		#"../Data/Chat Data/2007-04-21-#ubuntu.tsv",
		#"../Data/Chat Data/2007-04-22-#ubuntu.tsv",
		#"../Data/Chat Data/2007-10-19-#ubuntu.tsv",
		#"../Data/Chat Data/2007-10-20-#ubuntu.tsv",
		#"../Data/Chat Data/2007-10-21-#ubuntu.tsv",
		#"../Data/Chat Data/2008-04-25-#ubuntu.tsv",
		#"../Data/Chat Data/2008-04-26-#ubuntu.tsv",
	    ]

	    data_classes = ['positive', 'negative', 'neutral']

	    dataCollection = GetDataUbuntu(filenames,selected_features, data_classes)

	    print('Extracting features...')

	    training_features = np.array(dataCollection.get_feature_matrix())
	    training_features_per_user = dataCollection.get_feature_matrix_per_user()
	    training_labels_per_user = dataCollection.get_labels_per_user()

	    test_features = np.array(dataCollection.get_test_feature_matrix())
	    test_features_per_user = dataCollection.get_test_feature_matrix_per_user()
	    test_labels_per_user = dataCollection.get_test_labels_per_user()

	    # Find cluster centers
	    print('Clustering...')

	    cluster_centers, assignment = Clustering.cluster_feature_matrix(training_features, number_of_clusters)

	    assignments = []
	    for sequences in training_features_per_user:
		sentence_assignment = Clustering.get_nearest_clusters_matrix(cluster_centers, sequences)
		sentence_assignment = [each+1 for each in sentence_assignment]
		assignments.append(sentence_assignment)

	    # build HMM model
	    model = HMM(number_of_clusters, data_classes)

	    for i in range(0, len(assignments)):
		assignment = assignments[i]
		training_label = training_labels_per_user[i]
		transition_probability, emission_probability = model.add_data(assignment, training_label)

	    # testing
	    print "Now Testing with Training & Test Data"
	    print ""

	    # training data
	    training_assignments = []
	    training_sumaccuracy = 0
	    for sequences in training_features_per_user:
		sentence_assignment = Clustering.get_nearest_clusters_matrix(cluster_centers, sequences)
		sentence_assignment = [each+1 for each in sentence_assignment]
		training_assignments.append(sentence_assignment)

	    for i in range(0, len(training_assignments)):
		observations = training_assignments[i]
		training_label = training_labels_per_user[i]

		final_score, final_path = decoding.decoding(
		    observations = observations,
		    transition = transition_probability,
		    emission = emission_probability
		    )

		count = 0
		for j in range(0,len(final_path)):
		    if final_path[j] == training_label[j]:
		        count += 1

		accuracy = 100.0 * count / len(final_path)
		training_sumaccuracy += accuracy

	    # test data
	    test_assignments = []
	    test_sumaccuracy = 0
	    for sequences in test_features_per_user:
		sentence_assignment = Clustering.get_nearest_clusters_matrix(cluster_centers, sequences)
		sentence_assignment = [each+1 for each in sentence_assignment]
		test_assignments.append(sentence_assignment)

	    for i in range(0, len(test_assignments)):
		observations = test_assignments[i]
		test_label = test_labels_per_user[i]

		final_score, final_path = decoding.decoding(
		    observations = observations,
		    transition = transition_probability,
		    emission = emission_probability
		    )

		count = 0
		for j in range(0,len(final_path)):
		    if final_path[j] == test_label[j]:
		        count += 1

		accuracy = 100.0 * count / len(final_path)
		test_sumaccuracy += accuracy

		# print '-------------------------------'
		# print 'final score:', final_score
		# print 'final path:', final_path
		# print 'true path:', test_label
		# print 'accuracy', accuracy
		# print '-------------------------------'


	    result = test_sumaccuracy / len(test_assignments)
	    avg_accuracies.append(result)
	    print '-------------------------------'
	    print "average testing accuracy", result
	    print "average training  accuracy", training_sumaccuracy / len(training_assignments)
	    print '-------------------------------'

    print "overall acc: ", sum(avg_accuracies)/len(avg_accuracies)
    print "we have: ", avg_accuracies
    print "cluster centers: ", number_of_clusters

