        
'''''
We want the data to look like this at the end:
    total_counts = {start: {start: 0, 'p': 3, 'n': 5....}, 'p': {start: 2, 'p': 5....}, ... , last_label: {start: 1, ... }}
    transition_probs = {start: {start: count/
    emition_counts = {{
'''''        
    
    

class HMM:
    def __init__(self, number_of_clusters , labels):
        
        self.states = ['start'] + labels
        self.labels = labels
        self.number_of_clusters = number_of_clusters
        
        self.total_transition_counts = {state: {trans_state: 0 for trans_state in self.states} for state in self.states}     
        self.transition_probs = {state: {trans_state: 0 for trans_state in self.states} for state in self.states} 
        
        self.total_emission_counts = {label: {cluster: 0 for cluster in range(1, number_of_clusters+1)} for label in self.labels}
        self.emission_probs = {label: {cluster: 0 for cluster in range(1, number_of_clusters+1)} for label in self.labels}
        
    

    
    def add_data(self, data, labels):
        
        # Initialize the dict for the current transition counts. 
        # Count a transition from start to the first label and from the last label back to start.
        current_transition_counts = {state: {trans_state: 0 for trans_state in self.states} for state in self.states}
        current_transition_counts['start'][labels[0]] += 1
        current_transition_counts[labels[len(labels)-1]]['start'] += 1
        
        # Count all observed transitions from one label to another
        for i in range(0, len(labels)-1):
            old_state = labels[i]
            new_state = labels[i+1]
            current_transition_counts[old_state][new_state] += 1    
        
        # Update the total_transition_counts
        self.total_transition_counts = {
                state: {trans_state: self.total_transition_counts[state][trans_state] + current_transition_counts[state][trans_state] 
                    for trans_state in self.states} for state in self.states}
        
        # Update the probabilities 
        # Be careful not to devide by 0!!
        for state in self.total_transition_counts.keys():
            print 'state', state
            total = float(sum((self.total_transition_counts[state]).values()))
            if total > 0:
                self.transition_probs[state] = {trans_state: self.total_transition_counts[state][trans_state]/total for trans_state in self.states}
        
        
        # Initialize the dict for the current emission counts:
        current_emission_counts = {label: {cluster: 0 for cluster in range(1, self.number_of_clusters+1)} for label in self.labels}
         
        
        # Count all observed emissions of words in labels:
        
        for i in range(0, len(labels)):
            current_emission_counts[labels[i]][data[i]] += 1
        
        # Update the total_emission_counts
        self.total_emission_counts = {
                label: {cluster: self.total_emission_counts[label][cluster] + current_emission_counts[label][cluster] 
                    for cluster in range(1, self.number_of_clusters+1)} for label in self.labels}
        
        
        
        # Update the probabilities
        # Be careful not to devide by 0!!
        for state in self.total_emission_counts.keys():
            print 'state', state
            total = float(sum((self.total_emission_counts[state]).values()))
            if total > 0:
                self.emission_probs[state] = {cluster: self.total_emission_counts[state][cluster]/total for cluster in range(1, self.number_of_clusters+1)}
        
        print 'Transition counts:', self.total_transition_counts
        print 'Transition probs:', self.transition_probs
        print 'Emission counts:', self.total_emission_counts
        print 'Emission probs:', self.emission_probs
        
        
model = HMM(15, ['p', 'n'])
model.add_data([1, 5, 2, 7], ['n', 'n', 'n', 'n'])
