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
import pdb       
from HMM import HMM
import decoding




if __name__ == "__main__":
    training_percentage = 1
    
    '''
    # Reading
    '''

    n_per_class = 100
    
    data_class = [
        ['../Data/Twitter/hc1', 0, ';-)'],
        ['../Data/Twitter/hc2', 1, ';D'],
        ['../Data/Twitter/hc3', 2, ';)'],
        #['../Data/Twitter/hc4', 3, ';-D'],
        #['../Data/Twitter/hc5', 4, ';-P'],
        #['../Data/Twitter/hc6', 5, ';P'],
        #['../Data/Twitter/hc7', 6, ';-('],
        #['../Data/Twitter/hc8', 7, ';('],
        #['../Data/Twitter/hc9', 8, ';o'],
        #['../Data/Twitter/hc10', 9, ';]'],
        #['../Data/Twitter/hc11', 10, '=]'],
        #['../Data/Twitter/hc13', 11, ';*'],
        #['../Data/Twitter/hc15', 12, ';|'],
        #['../Data/Twitter/hc_non', 13, '_non_'],
    ]
    
    
    
    #data_class = [
    #    ['../Data/Chat Data/2006-05-27-#ubuntu.tsv', 0, ':(']
    # ]

#
#    pdb.set_trace()    
    
    # load data from tsv and build data collection
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
    cluster_centers, assignment = Clustering.cluster_feature_matrix(training_features, number_of_clusters)
    
     
    # Because the clusters are 0-14 and I want them 1:15 :P :P Gonna fix this..   
    assignment = [each+1 for each in assignment]             
       
    data_classes = [0, 1, 2]   
    model = HMM(number_of_clusters, data_classes)
    print 'size assinment: ', len(assignment)
    print 'assignment', assignment
    print 'size labels', len(training_label)
    print 'lables', training_label
    transition_probability, emission_probability = model.add_data(assignment, training_label)
    
    observations = assignment
 
    final_score, final_path = decoding.decoding(
        #states,
        observations = observations,
        transition = transition_probability,
        emission = emission_probability
        )

    print 'final score:', final_score
    print 'final path:', final_path

    print 'true path:', training_label