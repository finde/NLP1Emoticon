import json
import argparse
import re
from string import punctuation
import nltk
from Dictionary import positive_words, negative_words



class DataPoint:
    def __init__(self, data_string, hashtags, class_label):
        self.data_string = data_string
        self.hashtags = hashtags
        self.class_label = class_label



#####################
# Basic class funcs #
#####################

    def get_data_string(self):
            return self.data_string

    def get_hashtags(self):
            return self.hashtags

    def get_class_label(self):
            return self.class_label

    def get_positive_words(self):
            return positive_words

    def get_negative_words(self):
            return negative_words

    def get_list_of_words(self):
            return self.data_string.split()


    def print_data_point(self):
            print "TEXT: ", self.get_data_string()
            print "HASHTAGS: ", self.get_hashtags()
            print "CLASS: ", self.get_class_label()


############################
# Feature extraction funcs #
############################


    # Count total number of words
    # from given array of words
    def count_words(self):
            # Split the string into seperate words and count them:
            words = self.split_sentence()
            return len(words)


    # Count number of positive words
    # from given array of words
    def count_positive_words(self):
        list_words = self.split_sentence(lowercase = True)
        return self.count_specific_words(list_words, self.get_positive_words())

    # Count number of negative words
    # from given array of words
    def count_negative_words(self):
        list_words = self.split_sentence(lowercase = True)
        return self.count_specific_words(list_words, self.get_negative_words())


    # Count number of positive words
    # from given array of hashtags
    def count_positive_words_in_hashtags(self):
        hashtags = self.get_lowercase_hashtags()
        return self.count_specific_words_in_hashtags(hashtags, self.get_positive_words())

    # Count number of negative words
    # from given array of hashtags
    def count_negative_words_in_hashtags(self):
        hashtags = self.get_lowercase_hashtags()
        return self.count_specific_words_in_hashtags(hashtags, self.get_negative_words())

    # Count number of uppercase words
    # maybe Ignore short words (I is always uppercase)
    def count_uppercase_words(self):
        n_words = 0

        for word in self.split_sentence():
            if word.isupper() and len(word)>1:
                n_words += 1

        return n_words

    # Count number of special punctuation occurrences
    def count_special_punctuation(self):
        # Count the number of special puncuation marks:
        exclamation_marks = self.get_data_string().count("!")
        question_marks = self.get_data_string().count("!")

        count_special_punctuation = exclamation_marks + question_marks
        return count_special_punctuation

    # Example function for counting types of tags:
    def count_adjectives(self):
        # Count the number of adjectives in a sentence
        return self.count_specific_type_in_tags('JJ')

########################################
# Help functions for eature extraction #
########################################


    '''
    For some functions we need the words to be all in lowercase.
    E.g. Happily is not in the list of positive words, happily is.
    Boolean argument added for this!
    Default would be false, so that we don't waste time for it unless
    it is really necessary
    '''
    '''
    Now punctuation option is also added.
    By default we would return the sentence without punctuation,
    since this (I guess..) what we usually want when we split the sentence
    '''
    # Split sentence into array words
    def split_sentence(self, lowercase=False, without_punctuation = True):
        if without_punctuation:
            data = self.get_sentence_without_punctuation()
        else:
            data = self.get_data_string()

        if lowercase:
            data = data.lower()

        list_words = re.findall(r"[\w']+|[.,!?;]", data)

        return list_words


    # Count words from given dictionary
    def count_specific_words(self, list_words, dictionary):
        n_words = 0

        for word in list_words:
            if word in dictionary:
                n_words += 1

        return n_words

    # Count number of specific words in a hashtag
    def count_specific_words_in_single_hashtag(self, hashtag, dictionary, repetition = False):
        n_words = 0
        match_words = []

        # Either count each occurence
        if repetition:
            for word in dictionary:
                n_words += hashtag.count(word)

        # Or just check for each word if it's in the hashtag or not
        else:
            for word in dictionary:
                if word in hashtag:
                    if len(match_words) == 0:
                        match_words.append(word)
                    else:
                        # check if any subset of found word is already stored before
                        for idx, match_word in enumerate(match_words):
                            if match_word in word:
                                match_words[idx] = word
                            else:
                                match_words.append(word)

            n_words = len(match_words)

        return n_words


    def count_specific_words_in_hashtags(self, hashtags, dictionary, repetition = False):
        n_words = 0

        for each in hashtags:
            n_words += self.count_specific_words_in_single_hashtag(each, dictionary, repetition)

        return n_words


    # Get the sentence without punctuation
    def get_sentence_without_punctuation(self):
        sentence_without_punctuation = ' '.join(word.strip(punctuation) for word in self.get_data_string().split()
             if word.strip(punctuation))
        return sentence_without_punctuation


    # Turn hashtags into lowercase for matching in the
    def get_lowercase_hashtags(self):
        if self.get_hashtags() is None:
            return []
        else:
            return [each.lower() for each in self.get_hashtags()]


    # Tag a "tokenized" list of words
    # Keep puntuation, pos_tag would also tag it.
    # Turn to lowercase, otherwise there are mistakes
#### TODO: Apperantly it's weird even with lowercase
#### ('try' is not and adjective (JJ) for sure..)
#### Check how to properly use the pos_tag function!!!
    def pos_tag_data_string(self):
        split = self.split_sentence(lowercase=True, without_punctuation=False)
        return nltk.pos_tag(split)


    # Counts the number of tags from specific type
    def count_specific_type_in_tags(self, type):
        count = 0
        for each in self.pos_tag_data_string():
            if each[1] == type:
                count += 1

        return count

    # Count the number of tags from a whole list of POS tags
    def count_multiple_types_in_tags(self, types):
        count = 0
        for each in types:
            count += self.count_specific_type_in_tags(each)
        return count


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
        data_string = vars(args)['text']
    else:
        data_string = "What's going on if I Happily try to do this SAD thing?!"

    if(vars(args)['hashtags'] is not None):
        hashtags = vars(args)['hashtags']
    else:
        hashtags = ["#FeelingProductive", "#LifeIsSoAwesome", "#NLPSUCKS", "#sohappy"]

    if(vars(args)['class'] is not None):
        data_class = vars(args)['class']
    else:
        data_class = 0


    # Construct a data point:
    data_point = DataPoint(data_string, hashtags, data_class)


    # Do some random shit to make sure things work :)

    print "This is your data: \n ", data_point.get_data_string()
    print "This is your data splitted 1st way (get_list_of_words()): \n ", data_point.get_list_of_words()
    print "This is your data splitted 2nd way (split_sentence()): \n ", data_point.split_sentence()
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


    print "This is your data tagged in a mysterious way: \n ", data_point.pos_tag_data_string()
    print "Number of adjectives (JJ): ", data_point.count_adjectives()
    # Example for counting more than one part of speech:
    print "Number of adjectives (JJ) and adverbs (RB): ", data_point.count_multiple_types_in_tags(['JJ', 'RB'])


    data_point.print_data_point()



    print punctuation