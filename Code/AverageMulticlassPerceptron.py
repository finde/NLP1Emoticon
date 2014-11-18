# Source algorithm http://stp.lingfil.uu.se/~nivre/master/ml2.html
#class AverageMulticlassPerceptron:
#    def __init__(self, training_data):
import numpy as np
import TrainingData
from Dictionary import Dictionary
import DataPoint
from TSVParser import TSV_Getter

def mlp_gradient(x, t, w, b, v, a, L, number_classes):
    # initialize datastructures w, b, v and a to fill later on
    gradW = np.zeros((L, number_classes));
    gradB = np.zeros(number_classes);
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
    for j in range (0, number_classes):
        gradB[j] = ((j == t) - np.exp(logQ[j] - logZ));
        gradW[:,j] = h * gradB[j];
    
    #compute deltaH and compute gradients
    deltaH = w.dot(gradB);
    gradA = deltaH.T*h*(1-h);
    gradV = np.outer(x,(deltaH.T*h*(1-h)));
    
    #return gradients
    return gradW, gradB, gradA, gradV

def mlp_iter(x_train, t_train, w, b, v, a, L, number_classes):
    # create a number of indices
    r = list(range(x_train.shape[0]));
    
    # shuffle numbers in r to iterate over our trainingset in a random way
    np.random.shuffle(r);
    for row in r:
        gradW, gradB, gradA, gradV = mlp_gradient(x_train[row, :], t_train[row], w, b, v, a, L, number_classes);
        
        # update gradients, but multiply by small learning rate to keep the weights small
        w = w + gradW*(1E-1);
        b = b + gradB*(1E-1);
        v = v + gradV*(1E-1);
        a = a + gradA*(1E-1);
    return w, b, v, a

def mlp_train_set(w, b, v, a, N, L, x_train, t_train, number_classes):
    for i in range(0, N):
        w, b, v, a = mlp_iter(x_train, t_train, w, b, v, a, L, number_classes);
    return w, b, v, a

def count_correct_results(w, b, v, a, x_test, t_test, number_classes):
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
        print classification, t_test[i], ' '
        if(classification == t_test[i]):
            cnt = cnt + 1;
    return cnt, t_test.shape[0]
   
if __name__ == "__main__":
#    training_data = get_training_data()
#    AMP = AverageMulticlassPerceptron(training_data)
    L = 2;
    N = 50;
    number_classes = 2
    
    
    data_string = ["This is a second AWesOme example and i LOVE it?!", "I feel sad", "I don't care"]
    hashtags = [["#happy", "#yay", "#love"],
        ["#sad", "#depressed", "#suicidemood", "#totallyhungry"],
        ["#whatever"]]

    data_class = np.array([0, 1, 2])
    dictionary = Dictionary()
    
    #data_points = [DataPoint.DataPoint(data_string[i], hashtags[i], data_class[i], dictionary) for i in range(0, len(data_class))]
    
    data_class = [
        ['negative.tsv', 0],
        ['positive.tsv', 1]
    ]
    
    data_points = []
    for c in data_class:
        data_points = data_points + [DataPoint.DataPoint(_.text, _.hashtags, c[1], dictionary) for _ in
                                     TSV_Getter(c[0]).get_all_tsv_objects(50)]
    
    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)    
    
    training_data.print_data()
    print training_data.get_feature_dictionary()
    print training_data.get_label_vector()
    # Get the feature matrix of this data
    feat_matrix = np.array(training_data.get_feature_matrix())
    
    
    
    x_train = feat_matrix
    t_train = np.array(training_data.get_label_vector())
    
    #start with really small weights!!
    w = np.random.randn(L, number_classes)*0.015; 
    b = np.random.randn(number_classes)*0.0015; 
    v = np.random.randn(8, L)*0.015;
    a = np.random.randn(L)*0.0015; 
    
    
    
    w, b, v, a = mlp_train_set(w, b, v, a, N, L, x_train, t_train, number_classes);
    cnt, cntall = count_correct_results(w, b, v, a, x_train, t_train, number_classes);
    print 'cnt: ', cnt, '\n cntall: ', cntall