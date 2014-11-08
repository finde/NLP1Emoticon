import os
import json
import re
import language_check  # https://pypi.python.org/pypi/language-check
import ftfy  # http://ftfy.readthedocs.org/en/latest/
import progressbar


class Preprocessor:
    def __init__(self, class_label):
        filename = class_label + '_raw.json'
        self.filename = class_label + '.json'

        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            # load json dump into variable
            f = open(filename, 'r')
            self.statuses = json.load(f)
            f.close()

    @staticmethod
    def remove_hashtags(text):
        hashtags = [tag.strip("#") for tag in text.split() if tag.startswith("#")]
        clean_text = re.sub(r'#(\w+)', r'\1', text)
        return clean_text, hashtags

    @staticmethod
    def language_corrector(text):
        lang_tool = language_check.LanguageTool('en-US')
        return language_check.correct(text, lang_tool.check(text))

    @staticmethod
    def remove_unicode(text):
        text = ftfy.fix_text(text)
        return text.encode('ascii', 'ignore').decode('utf-8')

    @staticmethod
    def remove_html(text):
        return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '@HLINK', text)

    @staticmethod
    def remove_retweet(text):
        if text.find("RT ") == 0:
            return text.replace("RT ", "")
        return text

    def process_text(self, text):

        # removing hashtags
        text, hashtags = self.remove_hashtags(text)

        # remove unicode like \u03c0
        text = self.remove_unicode(text)

        # replace HTML link with @HLINK
        text = self.remove_html(text)

        # spellchecker
        text = self.language_corrector(text)

        # remove RT
        text = self.remove_retweet(text)

        return {
            'hashtags': hashtags,
            'text': text
        }

    def run(self):
        print 'Emoticon: ', emoticon

        bar = progressbar.ProgressBar(maxval=len(self.statuses),
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        i = 0
        if self.statuses:
            new_statuses = []
            for status in self.statuses:
                print "\n\nbefore: ", status
                status = self.process_text(status)

                print "after: ", status
                new_statuses.append(status)

                i += 1
                bar.update(i)

                # write and close every iteration, so we at least reach something when error happen
                f = open(self.filename, 'w+')
                f.write(json.dumps(new_statuses))
                f.close()

        bar.finish()


if __name__ == "__main__":
    for emoticon in ['positive', 'negative']:
        Preprocessor(emoticon).run()