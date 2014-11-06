import json
import pdb
from pprint import pprint

'''Feature extraction class'''
class Json_Object:    
    # Store json object
    # One Json_Object per tweet
    # Store in array/vector for later use!
    def __init__(self, json_object):
        #open file here and store as string
        self.json_object = json.loads(json_object)
        
    # Get raw text from json object
    def get_raw(self): 
        return self.json_object["raw"]
 
    # Get clean text from json object
    def get_clean(self): 
        return self.json_object["text"]
    
    # Get emoticons from json object
    def get_emoticons(self): 
        emoticons = []
        for key in self.json_object["emoticons"]:
            emoticons.append(key.encode("utf-8"))
        return emoticons
    
    # Get hashtags from json object
    def get_tags(self): 
        tags = []
        for key in self.json_object["tags"]:
            tags.append(key.encode("utf-8"))
        return tags
                      
if __name__ == "__main__":
	# Get json file
	# File contains array of tweets
	# Loop through file
	# Store json object in vector
	
	json_objects = []
	
	j_son = json.dumps({"raw": "raw text", "text": "clean text", "emoticons": [":)", ":(", ":|"], "tags": ["happy", "sad", "neutral"]},{"raw": "raw new text", "text": "clean new text", "emoticons": [":D", "D:", ":-|"], "tags": ["less", "more", "even"]})
	print j_son
        json_object = Json_Object(j_son)
        print 'raw: ', json_object.get_raw()
        print 'clean: ', json_object.get_clean()
        print 'emoticons: ', json_object.get_emoticons()
        print 'tags: ', json_object.get_tags()
        