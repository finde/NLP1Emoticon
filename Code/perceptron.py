# Copyright (c) 2012 Leif Johnson <leif@leifjohnson.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import numpy as np
import TrainingData
from Dictionary import Dictionary
import DataPoint

import lmj.perceptron.averaged as AMP

if __name__ == "__main__":
#    features = [
#        [1, 1, 1],
#        [0, 0, 0],
#        [2, 2, 2]
#    ]
#    
#    
#    label = ['a', 'b', 'c']
#

    # Generate a couple of data strings, hashtags and classes
    data_string = ["This is a second AWesOme example and i LOVE it?!", "I feel sad", "I don't care"]
    hashtags = [["#happy", "#yay", "#love"],
        ["#sad", "#depressed", "#suicidemood", "#totallyhungry"],
        ["#whatever"]]
    data_class = [0, 1, 2]
    
    # open the dictionaries
    dictionary = Dictionary()
    
    # generate points from all the strings, hashtags, classes
    data_points = [DataPoint.DataPoint(data_string[i], hashtags[i], data_class[i], dictionary) for i in range(0, len(data_class))]
    
    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)    
    
    # Get the feature matrix of this data
    feat_matrix = training_data.get_feature_matrix()

    # these are now your features and your classes
    features = feat_matrix
    labels = data_class
        
    
    
    # perceptron = Perceptron()
    # perceptron.learn(features, label)

    multiclass = AMP.Multiclass()

    for n in xrange(10):
        for i in xrange(len(features)):
            multiclass.learn(features[i], labels[i])

    for i in xrange(len(features)):
        print multiclass.predict(features[i])
