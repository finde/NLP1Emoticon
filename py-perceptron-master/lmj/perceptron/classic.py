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


def score(features, weights):
    return sum(weights.get(f, 0) for f in features)


class Perceptron:
    def __init__(self):
        self.weights = collections.defaultdict(float)

    def learn(self, features, label):
        if self.predict(features) ^ bool(label):
            for f in features:
                self.weights[f] += 1

    def predict(self, features):
        return score(features, self.weights) > 0


class Multiclass(Perceptron):
    def __init__(self):
        self.weights = collections.defaultdict(
            lambda: collections.defaultdict(float))

    def learn(self, features, label):
        predicted = self.predict(features)
        if predicted != label:
            towa = self.weights[label]
            away = self.weights[predicted]
            for f in features:
                towa[f] += 1
                away[f] -= 1

    def predict(self, features):
        return max((score(features, ws), l) for l, ws in self.weights.iteritems())[1]
