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

import collections

NULL_LABEL = '__NULL_LABEL__'

def score(features, weights):
    return sum(weights.get(f, 0) for f in features)


class Perceptron:
    def __init__(self):
        self.weights = collections.defaultdict(float)
        self.edges = collections.defaultdict(float)
        self.count = 0

    def learn(self, features, label):
        if self.predict(features) ^ bool(label):
            for f in features:
                self.edges[f] += 1
        self.average()

    def predict(self, features):
        return score(features, self.weights) > 0

    def average(self):
        c = self.count
        for f, w in self.edges.iteritems():
            self.weights[f] = (c * self.weights[f] + w) / (c + 1)
        self.count += 1


class Multiclass(Perceptron):
    def __init__(self):
        self.weights = collections.defaultdict(
            lambda: collections.defaultdict(float))
        self.edges = collections.defaultdict(
            lambda: collections.defaultdict(float))
        self.count = 0

    def learn(self, features, label):
        toward = self.edges[label]
        predicted = self.predict(features, True)
        if predicted is NULL_LABEL:
            for f in features:
                toward[f] += 1
        elif predicted != label:
            away = self.edges[predicted]
            for f in features:
                toward[f] += 1
                away[f] -= 1
        self.average()

    def predict(self, features, edge=False):
        sources = self.weights
        if edge:
            sources = self.edges
        if not sources:
            return NULL_LABEL
        return max((score(features, ws), l) for l, ws in sources.iteritems())[1]

    def average(self):
        c = self.count
        for l, sources in self.edges.iteritems():
            targets = self.weights[l]
            for f, w in sources.iteritems():
                targets[f] = (c * targets[f] + w) / (c + 1)
        self.count += 1
