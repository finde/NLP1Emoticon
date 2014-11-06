import json
import argparse



class DataPoint:
	def __init__(self, data_string, class_label):
		self.data_string = data_string
		self.class_label = class_label
		
		
	
#####################
# Basic class funcs #
#####################
        
        def get_data_string(self):
                return self.data_string
                
        def get_class_label(self):
                return self.class_label
        
        def get_list_of_words(self):
                return self.data_string.split()                
                
        
############################
# Feature extraction funcs #
############################

        def get_word_count(self):
                # Split the string into seperate words and count them:
                words = self.get_list_of_words()
                return len(words)
                
        
        def get_special_punctuation_count(self):
                # Count the number of special puncuation marks:
                exclamation_marks = self.get_data_string().count("!")
                question_marks = self.get_data_string().count("!")
                
                count_special_punctuation = exclamation_marks + question_marks
                return count_special_punctuation
                
            
if __name__ == "__main__":
    
	#Command line arguments
	parser = argparse.ArgumentParser(description="Run simulation")
	
	parser.add_argument('-text', metavar='The text of the data point', type=str)
	parser.add_argument('-class', metavar='The class label of the data point (-1, 0, 1)', type=int)
	
	args = parser.parse_args()
 
        # If arguments are passed to the command line, assign them.
        # Otherwise, use some standart ones.
        if(vars(args)['text'] is not None):
		data_string = vars(args)['text']
        else: 
                data_string = "What's going on if I try to do this?!"
                
	if(vars(args)['class'] is not None):
		data_class = vars(args)['class']
        else:
                data_class = 0
                                
        
        # Construct a data point:                                                                                                                                                            
        data_point = DataPoint(data_string, data_class)
        
        
        # Do some random shit to make sure things work :) 
         
        print "This is your data: \n ", data_point.get_data_string() 
        print "The word count is: ", data_point.get_word_count() 
        print "The # of ? and ! is: ", data_point.get_special_punctuation_count()
            
                