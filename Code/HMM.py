        
'''''
We want the data to look like this at the end:
    total_counts = {start: {start: 0, 1: 3, 3: 5....}, 1: {start: 2, 1: 5....}, ... number_of_clusters: {start: 1, ... }}
    transition_probs = {start: {start: count/
'''''        
    
    

class HMM:
    def __init__(self, number_of_clusters, labels):
        
        self.states = ['start'] + labels
        self.total_counts = {state: {trans_state: 0 for trans_state in self.states} for state in self.states}
        
        for each in self.total_counts.keys():
            self.total_counts[each] = {state: 0 for state in self.total_counts.keys()}
                    
        self.transition_probs = dict()
        self.emission_probs = dict()
        
        self.labels = labels
        
    

    
    def add_data(self, data, labels):
        
        current_counts = {state: {trans_state: 0 for trans_state in self.states} for state in self.states}
        current_counts['start'][labels[0]] += 1
        
        for i in range(0, len(labels)-1):
            old_state = labels[i]
            new_state = labels[i+1]
            current_counts[old_state][new_state] += 1
        
        
        self.total_counts = {state: {trans_state: self.total_counts[state][trans_state] + current_counts[state][trans_state] for trans_state in self.states} for state in self.states}
        
        print self.total_counts
        
        
model = HMM(15, ['p', 'n'])
model.add_data([1, 5, 2, 7], ['p', 'n', 'n', 'n'])
