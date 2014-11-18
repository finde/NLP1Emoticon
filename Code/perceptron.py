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
from TSVParser import TSV_Getter

import lmj.perceptron.averaged as AMP

if __name__ == "__main__":
    # features = [
    # [1, 1, 1],
    # [0, 0, 0],
    # [2, 2, 2]
    # ]
    #
    #
    # label = ['a', 'b', 'c']
    #

    # Generate a couple of data strings, hashtags and classes
    data_class = [
        ['negative.tsv', ':('],
        ['positive.tsv', ':)']
    ]

    # open the dictionaries
    dictionary = Dictionary()

    # generate points from all the strings, hashtags, classes

    data_points = []
    for c in data_class:
        data_points = data_points + [DataPoint.DataPoint(_.text, _.hashtags, c[1], dictionary) for _ in
                                     TSV_Getter(c[0]).get_all_tsv_objects(50)]

    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)

    # Get the feature matrix of this data
    feat_matrix = training_data.get_feature_matrix()

    # these are now your features and your classes
    features = feat_matrix
    labels = [row[1] for row in data_class]



    # perceptron = Perceptron()
    # perceptron.learn(features, label)

    multiclass = AMP.Multiclass()

    for n in xrange(1000):
        for i in xrange(len(data_points)):
            multiclass.learn(features[i], data_points[i].get_class_label())

    count = 0
    for i in xrange(len(data_points)):
        if data_points[i].get_class_label() == multiclass.predict(features[i]):
            count = count + 1

    print count * 100.0 / len(data_points)
