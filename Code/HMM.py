        
'''''
We want the data to look like this at the end:
    total_counts = {start: {start: 0, 1: 3, 3: 5....}, 1: {start: 2, 1: 5....}, ... number_of_clusters: {start: 1, ... }}
    transition_probs = {start: {start: count/
'''''        
    
    

class HMM:
    def __init__(self):
        self.counts = dict()
        self.total_counts = {}
        self.total_counts['start'] = 0
        self.transition_probs = dict()
        self.emission_probs = dict()
        
    

    
    def add_data(self, data, labels):
        current_counts = {}
        current_counts['start'] = 0
        
        for each in set(labels):
            current_counts[each] = 0
            if each not in self.total_counts.keys():
                self.total_counts[each] = 0
            
        print current_counts
        self.total_counts = {self.total_counts[key] + current_counts[key] for key in current_counts.keys()}
        
        
model = HMM()
model.add_data([1, 5, 2, 7], ['p', 'n', 'n', 'n'])
