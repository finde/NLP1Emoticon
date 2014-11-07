import json
import argparse
import re
from string import punctuation
import nltk
from Dictionary import Dictionary
import DataPoint



class TrainingData:
    def __init__(self, data_points):
        self.data_points = data_points
        

    
            
#####################
# Basic class funcs #
#####################
                
    def get_training_points(self):
        return self.data_points
        
    def print_data(self):
        for each in self.data_points:
            each.print_data_point()   

            
############################
# Feature extraction funcs #
############################
                                    
    def count_words(self):
        return self.count_feature('words')
        
        
        


########################################
# Help functions for eature extraction #
########################################

    def count_feature(self, feature):
        if feature == 'words':
            return [each.count_words() for each in self.get_training_points()]
        
        elif feature == 'positive_words':
            return [each.count_positive_words() for each in self.get_training_points()]
        
        elif feature == 'negative_words':
            return [each.count_negative_words() for each in self.get_training_points()]
        
        elif feature == 'positive_words_hashtags':
            return [each.count_positive_words_in_hashtags() for each in self.get_training_points()]
        
        elif feature == 'negative_words_hashtags':
            return [each.count_negative_words_in_hashtags() for each in self.get_training_points()]
        
        elif feature == 'uppercase_words':
            return [each.count_uppercase_words() for each in self.get_training_points()]
        
        elif feature == 'special_punctuation':
            return [each.count_special_punctuation() for each in self.get_training_points()]
        
        elif feature == 'adjectives':
            return [each.count_adjectives() for each in self.get_training_points()]
        
        else:
            return ['unknown feature, bro! :( Give me another one!']    


                
if __name__ == "__main__":

    #Command line arguments
    parser = argparse.ArgumentParser(description="Run simulation")

    parser.add_argument('-text', metavar='The text of the data point', type=str)
    parser.add_argument('-hashtags', metavar='The text of the data point', type=list)
    parser.add_argument('-class', metavar='The class label of the data point (-1, 0, 1)', type=int)

    args = parser.parse_args()

    # If arguments are passed to the command line, assign them.
    # Otherwise, use some standart ones.
    if(vars(args)['text'] is not None):
        data_string1 = vars(args)['text']
    else:
        data_string1 = "What's going on if I Happily try to do this SAD thing?!"

    if(vars(args)['hashtags'] is not None):
        hashtags1 = vars(args)['hashtags']
    else:
        hashtags1 = ["#FeelingProductive", "#LifeIsSoAwesome", "#NLPSUCKS", "#sohappy"]

    if(vars(args)['class'] is not None):
      data_class1 = vars(args)['class']
    else:
      data_class1 = 1

    
    data_string2 = "This is a second AWesOme example and i LOVE it?!"
    hashtags2 = ["#ProjectBecomesAnnoying", "#MeSoSleepy", "#suicidemood", "#totallyhungry"]

    data_class2 = -1
    # Load dictionary of positive and negative words
    dictionary = Dictionary()


    # Construct a data point:
    data_point1 = DataPoint.DataPoint(data_string1, hashtags1, data_class1, dictionary)
    data_point2 = DataPoint.DataPoint(data_string2, hashtags2, data_class2, dictionary)

    data = [data_point1, data_point2]
    
    
    training_data = TrainingData(data)
    # Do some random shit to make sure things work :)
    
#### TODO for some stupid reason all other functions work here
#### except from print_data_point() 
#### (it says DataPoint instance has no attribute 'print_data_point' )
#### Does anybody happen to know why? It works fine in the DataPoint file
    print "This is your first data point: \n "
    #data_point1.print_data_point()
    print data_point1.get_data_string()
    print "This is your second data point: \n "
    #data_point2.print_data_point()
    print data_point2.get_data_string()
    print "number of words: \n ", training_data.count_words()
    
    

    '''
    print "This is your data splitted: \n ", data_point.split_sentence()
    print "This is your data without punctuation: \n ", data_point.get_sentence_without_punctuation()
    print "The word count is: ", data_point.count_words()
    print "The # of ? and ! is: ", data_point.count_special_punctuation()

    print "Number of positive words: ", data_point.count_positive_words()
    print "Number of negative words: ", data_point.count_negative_words()
    
    print "Number of uppercase words: ", data_point.count_uppercase_words()
  
    print "These are your hashtags: \n ", data_point.get_hashtags()
    print "These are your lowercase hashtags: \n ", data_point.get_lowercase_hashtags() 

#### TODO: printing the matching pos/neg words in hashtags shows that e.g. suck and sucks are found.
#### That's not cool, because they correspond to the same word in the hashtag.
#### If only the longer one is counted then: in "#suckyweather #lifesucks" only one of them
#### will be found, when it's two bad words. But if we keep counting both, we count twice
#### the same word as in the example below... Sooo... Needs some fix          
    print "Number of positive words in hashtags: \n ", data_point.count_positive_words_in_hashtags()
    print "Number of negative words in hashtags: \n ", data_point.count_negative_words_in_hashtags()
    
    
    print "This is your data tagged in a misterious way: \n ", data_point.pos_tag_data_string()
    print "Number of adjectives (JJ): ", data_point.count_adjectives()
    # Example for counting more than one part of speech:
    print "Number of adjectives (JJ) and adverbs (RB): ", data_point.count_multiple_types_in_tags(['JJ', 'RB'])
    '''
    