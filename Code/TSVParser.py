import csv
import pdb
from pprint import pprint

'''Feature extraction class'''
class TSV_Object:    
    # Store tsv object
    # One TSV object per tweet
    def __init__(self, tsv_object):
        self.tsv_object = tsv_object
	self.text =  tsv_object[0]
	self.hashtags = tsv_object[1]
	#self.emoticons = tsv_object[2]

    # Get raw text from tsv object
    def get_text(self): 
        return self.text
 
    # Get emoticons from tsv object
    def get_emoticons(self): 
        emoticons = []
	emoticons_array = self.emoticons.split(',')
	for emo in emoticons_array:
	    print 'emo: ', emo
	    emoticons.append(emo)
        return emoticons
    
    # Get hashtags from tsv object
    def get_tags(self): 
        tags = []
	hashtags = self.hashtags.split(',')
	for tag in hashtags:
	    print 'tag: ', tag
	    tags.append(tag)
        return tags
        
class TSV_Getter:
    def __init__(self, filename, verbose=0):
        self.all_tsv_objects = []
	
	# Read TSV file:
	with open(filename,'rb') as tsvIn:
	    tsvIn = csv.reader(tsvIn, delimiter='\t')
	    for row in tsvIn:
	        # Do not store the first row
	        if(row[0] == 'Text'):
		    continue
		# Create tsv object of row (which is one tweet)
		tsv_obj = TSV_Object(row)
		# Store all tsv objects of this file in this getter class
		self.all_tsv_objects.append(tsv_obj)
		
    def get_all_tsv_objects(self):
        return self.all_tsv_objects
                      
if __name__ == "__main__":
    tsv_getter = TSV_Getter('negative_tsv.tsv')