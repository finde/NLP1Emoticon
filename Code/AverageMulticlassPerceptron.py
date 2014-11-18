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
    gradV = np.zeros((8, L));
    gradA = np.zeros(L);

    # print x
    # calculate h
    h = 1/(1+np.exp(-(v.T.dot(x) + a)));
    
    # calculate gradient for w and b as usual, only logQ is a bit different than before, so the result will be different.
    logQ = (w.T.dot(h)).T + b;
    c = logQ.max();
    qc = np.exp(logQ - c);
    logZ = c + np.log(sum(qc));

    # store derivatives
    for j in range (0, 3):
        gradB[j] = ((j == t) - np.exp(logQ[j] - logZ));
        gradW[:,j] = h * gradB[j];
    
    #compute deltaH and compute gradients
    deltaH = w.dot(gradB);
    gradA = deltaH.T*h*(1-h);
    gradV = np.outer(x,(deltaH.T*h*(1-h)));
    
    #return gradients
    return gradW, gradB, gradA, gradV

def mlp_iter(x_train, t_train, w, b, v, a, L):
    # create a number of indices
    r = list(range(x_train.shape[0]));
    
    # shuffle numbers in r to iterate over our trainingset in a random way
    np.random.shuffle(r);
    for row in r:
        gradW, gradB, gradA, gradV = mlp_gradient(x_train[row, :], t_train[row], w, b, v, a, L);
        
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

def count_correct_results(w, b, v, a, x_test, t_test):
    x_test = x_train
    t_test = t_train
    h = 1/(1+np.exp(-(x_test.dot(v) + a)));
    
    # implement the gradients we derived
    logQ = (h.dot(w)) + b;
    q = np.exp(logQ);
    Z = sum(q);

    c = logQ.max();
    qc = np.exp(logQ - c);
    logZ = c + np.log(sum(qc));    
    
    logP = logQ - logZ;
    
    cnt = 0;
    
    # count number of correctly labeled images
    for i in range(t_test.shape[0]):
        classification = np.argmax(logP[i,:]);
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

    data_class = np.array([0, 1, 2])
    dictionary = Dictionary()
    
    data_points = [DataPoint.DataPoint(data_string[i], hashtags[i], data_class[i], dictionary) for i in range(0, len(data_class))]
    
    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)    
    
    # Get the feature matrix of this data
    feat_matrix = np.array(training_data.get_feature_matrix())
    
    
    
    x_train = feat_matrix
    t_train = np.array(training_data.get_label_vector())
    
    #start with really small weights!!
    w = np.random.randn(L, 3)*0.005; 
    b = np.random.randn(3)*0.05; 
    v = np.random.randn(8, L)*0.005;
    a = np.random.randn(L)*0.05; 
    
    w, b, v, a = mlp_train_set(w, b, v, a, N, L, x_train, t_train);
    cnt, cntall = count_correct_results(w, b, v, a, x_train, t_train);
    print 'cnt: ', cnt, '\n cntall: ', cntall