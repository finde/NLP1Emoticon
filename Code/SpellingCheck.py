# Class performs spelling check and improves sentence
# But when do we call this? Think about it!
# Reference: http://www.learnr.pro/content/16978-python-text-processing-with-nltk-20-cookbook/48#1310401930:53161.20821874979
# Reference: https://github.com/mattalcock/blog/blob/master/2012/12/5/python-spell-checker.rst
# http://norvig.com/spell-correct.html
import enchant
from enchant.checker import SpellChecker
from nltk.metrics import edit_distance
import re
import collections

import language_check


class SpellingCheck:
    def __init__(self, text):
        self.dictionary = enchant.Dict("en-US")
        self.spelling_checker = SpellChecker(self.dictionary)
        self.spelling_checker.set_text(text)
        self.max_dist = 2
        self.errors = self.check_text()

    def fix_text(self):
        for word in self.spelling_checker:
            print "error: ", word
            suggestion = self.replace_word(word)
            print 'suggestion: ', suggestion
            word.replace(suggestion)

    def check_text(self):
        error_words = []
        for error in self.spelling_checker:
            error_words.append(error.word)
        return error_words

    def select_suggestion(self):
        correct_words = []
        for word in self.errors:
            print "error word: ", word
            suggestion = self.replace_word(word)
            print "suggestion: ", suggestion
            correct_words.append(suggestion)
        return correct_words

    def replace_word(self, word):
        if self.dictionary.check(word):
            return word

        suggestions = self.dictionary.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]


if __name__ == "__main__":
    sentence = "Helo! Ths is vomment."
    checker = SpellingCheck(sentence)
    print checker.select_suggestion()
    print checker.spelling_checker.get_text()

    language_tool = language_check.LanguageTool("en-US")
    matches = language_tool.check(sentence)
    sentence = language_check.correct(sentence, matches)
    print sentence