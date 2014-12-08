import os
import numpy as np
import random
import TrainingData
import DataPoint
from TSVParser import TSV_Getter
import scipy.cluster.vq as cluster
import cPickle
from getData import GetData


# Cluster features, using K-means
def cluster_feature_matrix(feature_matrix, number_of_clusters):
    cluster_centers, assignment = cluster.kmeans2(data=feature_matrix, k=number_of_clusters, thresh=1e-07, minit='points')
    return cluster_centers, assignment


# Find nearest cluster center for given vector
def get_nearest_cluster_vector(clusters, vector):
    cluster_distance = 1000
    nearest_cluster = 0

    # Loop through clusters and find nearest cluster
    for i in range(0, len(clusters)):
        distance = vector - clusters[i]
        location_cluster = np.linalg.norm(distance)
        if location_cluster < cluster_distance:
            cluster_distance = location_cluster
            nearest_cluster = i
    return nearest_cluster


# Find nearest cluster center for matrix of vectors. Return cluster centers in a matrix
def get_nearest_clusters_matrix(clusters, matrix):
    nearest_clusters = []

    for vector in matrix:
        nearest_cluster = get_nearest_cluster_vector(clusters, vector)
        nearest_clusters.append(nearest_cluster)

    return nearest_clusters


if __name__ == "__main__":
        
    training_percentage = 1
    
    '''
    # Reading
    '''

    n_per_class = 100
    
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        #['../Data/Twitter/hc2', 1, ';D'],
        #['../Data/Twitter/hc3', 2, ';)'],
        #['../Data/Twitter/hc4', 3, ';-D'],
        #['../Data/Twitter/hc5', 4, ';-P'],
        #['../Data/Twitter/hc6', 5, ';P'],
        #['../Data/Twitter/hc7', 6, ';-('],
        ['../Data/Twitter/hc8', 7, ';('],
        ['../Data/Twitter/hc9', 8, ';o'],
        #['../Data/Twitter/hc10', 9, ';]'],
        #['../Data/Twitter/hc11', 10, '=]'],
        #['../Data/Twitter/hc13', 11, ';*'],
        #['../Data/Twitter/hc15', 12, ';|'],
        #['../Data/Twitter/hc_non', 13, '_non_'],
    ]
    
    #data_class = [
    #    ['2006-05-27-#ubuntu-negative.tsv', ':('],
    #    ['2006-05-27-#ubuntu-positive.tsv', ':)']
    # ]

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

    dataCollection = GetData(data_class, n_per_class, training_percentage, selected_features)

    # split data collection into training and test data
    training_data = dataCollection.get_training_data()
    training_label = np.array(dataCollection.get_training_label())
 
    print('Extracting features...')

    # Get the feature matrix of this data
    print(' extracting train_data')
    training_features = dataCollection.get_training_feature_matrix()

    number_classes = len(data_class)
    
    number_of_clusters = 50
    
    # Find cluster centers
    cluster_centers, assignment = cluster_feature_matrix(training_features, number_of_clusters)
    #nearest_clusters = get_nearest_clusters_matrix(cluster_centers, training_features)
    
        # Just checking if the clusters are sort of consistent:
    for i in range(0, number_of_clusters):
        assigned_data = [data_index for data_index in range(0, len(assignment)) if assignment[data_index] == i]
        print 'Cluster', i, 'contains:', [training_label[i] for i in assigned_data] 

    