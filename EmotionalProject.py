import json
import argparse
import re



class DataPoint:
    def __init__(self, data_string, hashtags, class_label, dictionary):
        self.data_string = data_string
        self.hashtags = hashtags
        self.class_label = class_label
        self.positive_words = dictionary.get_positive_words()
        self.negative_words = dictionary.get_negative_words()



#####################
# Basic class funcs #
#####################

    def get_data_string(self):
            return self.data_string

    def get_hashtags(self):
            return self.hashtags

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

    # Split sentence into array words
    def split_sentence(self):
        list_words = re.findall(r"[\w']+|[.,!?;]", self.get_data_string())
        return list_words

    # Count words from given dictionary
    def count_specific_words(self, list_words, dictionary):
        n_words = 0

        for word in list_words:
            if word in dictionary:
                n_words += 1

        return n_words

    # Count number of positive words
    # from given array of words
    def count_positive_words(self):
        list_words = self.split_sentence()
        return self.count_specific_words(list_words, self.positive_words)

    # Count number of negative words
    # from given array of words
    def count_negative_words(self):
        list_words = self.split_sentence()
        return self.count_specific_words(list_words, self.negative_words)


if __name__ == "__main__":

    #Command line arguments
    parser = argparse.ArgumentParser(description="Run simulation")

    parser.add_argument('-text', metavar='The text of the data point', type=str)
    parser.add_argument('-hashtags', metavar='The text of the data point', type=list)
    parser.add_argument('-class', metavar='The class label of the data point (-1, 0, 1)', type=int)

    args = parser.parse_args()

    from Dictionary import Dictionary

    # If arguments are passed to the command line, assign them.
    # Otherwise, use some standart ones.
    if(vars(args)['text'] is not None):
        data_string = vars(args)['text']
    else:
        data_string = "What's going on if I try to do this?!"

    if(vars(args)['hashtags'] is not None):
        hashtags = vars(args)['hashtags']
    else:
        hashtags = ["#FeelingProductive", "#LifeIsSoAwesome", "#NLPSUCKS"]

    if(vars(args)['class'] is not None):
      data_class = vars(args)['class']
    else:
      data_class = 0


    # Load dictionary of positive and negative words
    dictionary = Dictionary()

    # Construct a data point:
    data_point = DataPoint(data_string, hashtags, data_class, dictionary)


    # Do some random shit to make sure things work :)

    print "This is your data: \n ", data_point.get_data_string()
    print "These are your hashtags: \n ", data_point.get_hashtags()
    print "The word count is: ", data_point.get_word_count()
    print "The # of ? and ! is: ", data_point.get_special_punctuation_count()

    print "Number of positive words: ", data_point.count_positive_words()
    print "Number of negative words: ", data_point.count_negative_words()
