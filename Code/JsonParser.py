import json
import pdb
from pprint import pprint

'''Feature extraction class'''
class Json_Object:    
    # Store json object
    # One Json_Object per tweet
    def __init__(self, json_object):
        self.json_object = json_object
        
    # Get raw text from json object
    def get_raw(self): 
        return self.json_object["raw"]
 
    # Get clean text from json object
    def get_clean(self): 
        return self.json_object["text"]
    
    # Get emoticons from json object
    def get_emoticons(self): 
        emoticons = []
        
        # Put values in array by encoding with utf-8. 
        # Else we get the ugly u'String thing!
        for key in self.json_object["emoticons"]:
            emoticons.append(key.encode("utf-8"))
        return emoticons
    
    # Get hashtags from json object
    def get_tags(self): 
        tags = []
        
        # Put values in array by encoding with utf-8. 
        # Python appears to assume something else!
        # Else we get the ugly u'String thing!
        for key in self.json_object["tags"]:
            tags.append(key.encode("utf-8"))
        return tags
        
class Json_Getter:
    def __init__(self, verbose=0):
        self.json_objects = []
	
	j_son = json.dumps([{"raw": "raw text", "text": "clean text", "emoticons": [":)", ":(", ":|"], "tags": ["happy", "sad", "neutral"]},{"raw": "raw new text", "text": "clean new text", "emoticons": [":D", "D:", ":-|"], "tags": ["less", "more", "even"]}])
	if verbose == 1:
	   print j_son
	self.json_load = json.loads(j_son)
	
    def parse_json(self, verbose=0):	
	# Loop through file of tweets
	# Store json object in vector
	for j_obj in self.json_load:
	    tweet = Json_Object(j_obj)	    
	    if verbose == 1:
                print 'raw: ', tweet.get_raw()
                print 'clean: ', tweet.get_clean()
                print 'emoticons: ', tweet.get_emoticons()
                print 'tags: ', tweet.get_tags()
            self.json_objects.append(j_obj)
            
        return self.json_objects
                      
if __name__ == "__main__":
	# Get json file
	# File contains array of tweets
	json_getter = Json_Getter()
	json_objects = json_getter.parse_json()