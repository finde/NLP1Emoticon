import os
import numpy as np
import random
import TrainingData
from Dictionary import Dictionary
import DataPoint
from TSVParser import TSV_Getter
from scipy.cluster.vq import *
import cPickle

# Cluster features, using K-means
def cluster_feature_matrix(feature_matrix, number_of_clusters):
    cluster_centers, irrelevant = kmeans2(feature_matrix, number_of_clusters)
    return cluster_centers


# Find nearest cluster center for given vector
def get_nearest_cluster_vector(clusters, vector):
    cluster_distance = 1000
    nearest_cluster = 0

    # Loop through clusters and find nearest cluster
    for center in clusters:
        distance = vector - center
        location_cluster = np.linalg.norm(distance)
        if location_cluster < cluster_distance:
            cluster_distance = location_cluster
            nearest_cluster = center
    return nearest_cluster


# Find nearest cluster center for matrix of vectors. Return cluster centers in a matrix
def get_nearest_clusters_matrix(clusters, matrix):
    nearest_clusters = []

    for vector in matrix:
        nearest_cluster = get_nearest_cluster_vector(clusters, vector)
        nearest_clusters.append(nearest_cluster)

    return nearest_clusters


if __name__ == "__main__":
    # load dictionary
    dictionary = Dictionary()

    # get data
    print('Reading data...')
    data_class = [  # ['../Data/Twitter/hc1', 0, ';-)'],
                    ['../Data/Twitter/hc2', 0, ';D'],
                    ['../Data/Twitter/hc3', 1, ';)'],  # ['../Data/Twitter/hc4', 3, ';-D'],
                    # ['../Data/Twitter/hc5', 4, ';-P'],  # ['../Data/Twitter/hc6', 5, ';P'],
                    # ['../Data/Twitter/hc7', 6, ';-('],  # ['../Data/Twitter/hc8', 7, ';('],
                    # ['../Data/Twitter/hc9', 8, ';o'],  # ['../Data/Twitter/hc10', 9, ';]'],
                    # ['../Data/Twitter/hc11', 10, '=]'],  # ['../Data/Twitter/hc13', 11, ';*'],
                    # ['../Data/Twitter/hc15', 12, ';|'],  # ['../Data/Twitter/hc_non', 13, '_non_'],
    ]

    # get data points
    data_points = []
    amount_data_per_class = 300

    for c in data_class:
        # comment line below for balanced data source
        amount_data_per_class = None
        data_points = data_points + [DataPoint.DataPoint(_.text, _.hashtags, c[1], dictionary) for _ in
                                     TSV_Getter(c[0]).get_all_tsv_objects(amount_data_per_class)]

    print('Feature extraction...')
    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)

    # Get the feature matrix of this data
    # filename = '../Data/Twitter/cache.__' + `len(data_class)` + '-Emo__.p'
    # if os.path.isfile(filename) and os.access(filename, os.R_OK):
    # fh = open(filename, "rb")
    # 	feat_matrix = cPickle.load(fh)
    # 	fh.close()
    # else:
    # 	fh = open(filename, "wb")
    feat_matrix = np.array(training_data.get_feature_matrix())
    # cPickle.dump(feat_matrix, fh)
    # fh.close()x   

    number_of_clusters = 15
    # Find cluster centers
    cluster_centers = cluster_feature_matrix(feat_matrix, number_of_clusters)
    nearest_clusters = get_nearest_clusters_matrix(cluster_centers, feat_matrix)

    # print nearest clusters. use only for testing purposes!
    # print "nearest clusters: ", nearest_clusters