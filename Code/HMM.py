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
        
                        
'''''
We want the data to look like this at the end:
    total_counts = {start: {start: 0, 'p': 3, 'n': 5....}, 'p': {start: 2, 'p': 5....}, ... , last_label: {start: 1, ... }}
    transition_probs = {start: {start: count/
    emition_counts = {{
'''''        

class HMM:
    def __init__(self, number_of_clusters , labels):
        
        self.labels = labels
        self.number_of_clusters = number_of_clusters
        
        self.transition_counts = {state: {trans_state: 0 for trans_state in self.get_states()} for state in self.get_states()}     
        self.transition_probs = {state: {trans_state: 0 for trans_state in self.get_states()} for state in self.get_states()} 
        
        self.emission_counts = {label: {cluster: 0 for cluster in range(1, number_of_clusters+1)} for label in self.labels}
        self.emission_probs = {label: {cluster: 0 for cluster in range(1, number_of_clusters+1)} for label in self.labels}
        
    
    # Labels 
    def get_labels(self):
        return self.labels
        
    # Labels + the 'start' state!    
    def get_states(self):
        return ['start'] + self.get_labels()
    
    def get_number_of_clusters(self):
        return self.number_of_clusters
    
    def update_transitions_probs(self):
        # Be careful not to devide by 0!!
        for state in self.transition_counts.keys():
            total = float(sum((self.transition_counts[state]).values()))
            if total > 0:
                self.transition_probs[state] = {trans_state: self.transition_counts[state][trans_state]/total 
                                                    for trans_state in self.get_states()}
    
        
    def update_emission_probs(self):
        # Be careful not to devide by 0!!
        for state in self.emission_counts.keys():
            total = float(sum((self.emission_counts[state]).values()))
            if total > 0:
                self.emission_probs[state] = {cluster: self.emission_counts[state][cluster]/total 
                                                for cluster in range(1, self.number_of_clusters+1)}
            
    
    def add_data(self, data, labels):
        
        # Initialize the dict for the current transition counts. 
        # Count a transition from start to the first label and from the last label back to start.
        current_transition_counts = {state: {trans_state: 0 for trans_state in self.get_states()} for state in self.get_states()}
        current_transition_counts['start'][labels[0]] += 1
        current_transition_counts[labels[len(labels)-1]]['start'] += 1
        
        # Count all observed transitions from one label to another
        for i in range(0, len(labels)-1):
            old_state = labels[i]
            new_state = labels[i+1]
            current_transition_counts[old_state][new_state] += 1    
        
        # Update the total_transition_counts
        self.transition_counts = {
                state: {trans_state: self.transition_counts[state][trans_state] + current_transition_counts[state][trans_state] 
                    for trans_state in self.get_states()} for state in self.get_states()}
        
        # Update the probabilities 
        self.update_transitions_probs()
        
        # Initialize the dict for the current emission counts:
        current_emission_counts = {label: {cluster: 0 for cluster in range(1, self.number_of_clusters+1)} for label in self.labels}
        
        print current_emission_counts, self.emission_counts 
        
        # Count all observed emissions of words in labels:
        
        for i in range(0, len(labels)):
            current_emission_counts[labels[i]][data[i]] += 1
        
        # Update the total_emission_counts
        self.emission_counts = {
                label: {cluster: self.emission_counts[label][cluster] + current_emission_counts[label][cluster] 
                    for cluster in range(1, self.number_of_clusters+1)} for label in self.labels}
        
        
        
        # Update the probabilities
        self.update_emission_probs()
        
        
        print 'Transition counts:', self.transition_counts
        print 'Transition probs:', self.transition_probs
        print 'Emission counts:', self.emission_counts
        print 'Emission probs:', self.emission_probs
        


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
    cluster_centers, assignment = Clustering.cluster_feature_matrix(training_features, number_of_clusters)
    
     
    # Because the clusters are 0-14 and I want them 1:15 :P :P Gonna fix this..   
    assignment = [each+1 for each in assignment]             
       
    data_classes = [0, 1, 2]   
    model = HMM(number_of_clusters, data_classes)
    print 'size assinment: ', len(assignment)
    print 'assignment', assignment
    print 'size labels', len(training_label)
    print 'lables', training_label
    model.add_data(assignment, training_label)
 