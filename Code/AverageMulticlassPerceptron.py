# Source algorithm http://stp.lingfil.uu.se/~nivre/master/ml2.html
#class AverageMulticlassPerceptron:
#    def __init__(self, training_data):
import numpy as np
import TrainingData
from Dictionary import Dictionary
import DataPoint

def mlp_gradient(x, t, w, b, v, a, L):
    # initialize datastructures w, b, v and a to fill later on
    gradW = np.zeros((L, 3));
    gradB = np.zeros(3);
    gradV = np.zeros((10, L));
    gradA = np.zeros(L);

    # calculate h
    h = 1/(1+exp(-(v.T.dot(x) + a)));
    
    # calculate gradient for w and b as usual, only logQ is a bit different than before, so the result will be different.
    logQ = (w.T.dot(h)).T + b;
    c = logQ.max();
    qc = exp(logQ - c);
    logZ = c + log(sum(qc));

    # store derivatives
    for j in range (0, 3):
        gradB[j] = ((j == t) - exp(logQ[j] - logZ));
        gradW[:,j] = h * gradB[j];
    
    #compute deltaH and compute gradients
    deltaH = w.dot(gradB);
    gradA = deltaH.T*h*(1-h);
    gradV = outer(x,(deltaH.T*h*(1-h)));
    
    #return gradients
    return gradW, gradB, gradA, gradV

def mlp_iter(x_train, t_train, w, b, v, a, L):
    # create a number of indices
    r = list(range(x_train.shape[0]));
    
    # shuffle numbers in r to iterate over our trainingset in a random way
    random.shuffle(r);
    for row in r:
        gradW, gradB, gradA, gradV = mlp_gradient(x_train[row,:], t_train[row], w, b, v, a, L);
        
        # update gradients, but multiply by small learning rate to keep the weights small
        w = w + gradW*(1E-2);
        b = b + gradB*(1E-2);
        v = v + gradV*(1E-2);
        a = a + gradA*(1E-2);
    return w, b, v, a

def mlp_train_set(w, b, v, a, N, L, x_train, t_train):
    for i in range(0, N):
        w, b, v, a = mlp_iter(x_train, t_train, w, b, v, a, L);
    return w, b, v, a

def count_correct_results(w, b, v, a):
    h = 1/(1+exp(-(x_test.dot(v) + a)));
    
    # implement the gradients we derived
    logQ = (h.dot(w)) + b;
    q = exp(logQ);
    Z = sum(q);

    c = logQ.max();
    qc = exp(logQ - c);
    logZ = c + log(sum(qc));    
    
    logP = logQ - logZ;
    
    cnt = 0;
    
    # count number of correctly labeled images
    for i in range(t_test.shape[0]):
        classification = argmax(logP[i,:]);
        if(classification == t_test[i]):
            cnt = cnt + 1;
    return cnt, t_test.shape[0]
   
if __name__ == "__main__":
#    training_data = get_training_data()
#    AMP = AverageMulticlassPerceptron(training_data)
    L = 5;
    N = 5;
    
    data_string = ["This is a second AWesOme example and i LOVE it?!", "I feel sad", "I don't care"]
    hashtags = [["#happy", "#yay", "#love"],
        ["#sad", "#depressed", "#suicidemood", "#totallyhungry"],
        ["#whatever"]]

    data_class = [0, 1, 2]
    dictionary = Dictionary()
    
    data_point = np.zeros((len(data_class),1))
    for i in range(0, len(data_class)):
        data_point[i] = DataPoint.DataPoint(data_string[i], hashtags[i], data_class[i], dictionary)

    training_data = TrainingData(data_point)    
    feature_dict = training_data.get_feature_dictionary()
    
    feature_dict = training_data.get_feature_dictionary()
    feat_matrix = [[d[i] for d in feature_dict.values()] for i in range(0, len(feature_dict['adjectives']))]
    
    x_train = feat_matrix
    t_train = data_class
    
    #start with really small weights!!
    w = np.random.randn(L, 3)*0.0015; 
    b = np.random.randn(3)*0.015; 
    v = np.random.randn(10, L)*0.0015;
    a = np.random.randn(L)*0.0015; 
    
    w, b, v, a = mlp_train_set(w, b, v, a, N, L, x_train, t_train);
    cnt, cntall = count_correct_results(w, b, v, a);
    print 'cnt: ', cnt, '\n cntall: ', cntall