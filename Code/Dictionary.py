class Dictionary:
    FILE_POS = "../Data/Dictionary/positive-words.txt"
    FILE_NEG = "../Data/Dictionary/negative-words.txt"

    def __init__(self):
        self.positive_words = self.load_positive_words()
        self.negative_words = self.load_negative_words()

    # get list of positive words
    def get_positive_words(self):
        return self.positive_words

    # get list of positive words
    def get_negative_words(self):
        return self.negative_words


    # ===========================
    # Methods
    # ===========================

    def load_word_list(self, file):
        word_list = []
        idx = 0

        file = open(file, 'r')

        for line in file:
            if idx >= 36:
                line = line.rstrip('\n')
                word_list.append(line)
            idx += 1

        return word_list

    # Load list of positive words
    # save them into an array
    def load_positive_words(self):
        return self.load_word_list(self.FILE_POS)

    # Load list of negative words
    # save them into an array
    def load_negative_words(self):
        return self.load_word_list(self.FILE_NEG)



dictionary = Dictionary()
positive_words = dictionary.get_positive_words()
negative_words = dictionary.get_negative_words()
