# Source algorithm http://stp.lingfil.uu.se/~nivre/master/ml2.html
#class AverageMulticlassPerceptron:
#    def __init__(self, training_data):
import numpy as np
import random
import TrainingData
from Dictionary import Dictionary
import DataPoint
from TSVParser import TSV_Getter

def mlp_gradient(x, t, w, b, v, a, L, number_classes,number_features):
    # initialize datastructures w, b, v and a to fill later on
    gradW = np.zeros((L, number_classes));
    gradB = np.zeros(number_classes);
    gradV = np.zeros((number_features, L));
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

def mlp_iter(x_train, t_train, w, b, v, a, L, number_classes, number_features):
    # create a number of indices
    r = list(range(x_train.shape[0]));
    
    # shuffle numbers in r to iterate over our trainingset in a random way
    np.random.shuffle(r);
    for row in r:
        gradW, gradB, gradA, gradV = mlp_gradient(x_train[row, :], t_train[row], w, b, v, a, L, number_classes, number_features);
        
        # update gradients, but multiply by small learning rate to keep the weights small
        w = w + gradW*(1E-1);
        b = b + gradB*(1E-1);
        v = v + gradV*(1E-1);
        a = a + gradA*(1E-1);
    return w, b, v, a

def mlp_train_set(w, b, v, a, N, L, x_train, t_train, number_classes, number_features):
    for i in range(0, N):
        w, b, v, a = mlp_iter(x_train, t_train, w, b, v, a, L, number_classes, number_features);
    return w, b, v, a

def count_correct_results(w, b, v, a, x_test, t_test):

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
# TODO: These probabilities seem weird, find out if that's expected behaviour
        print classification, t_test[i], np.exp(logP[i,:]), ' '
        if(classification == t_test[i]):
            cnt = cnt + 1;
    return cnt, t_test.shape[0]
   
if __name__ == "__main__":
#    training_data = get_training_data()
#    AMP = AverageMulticlassPerceptron(training_data)
    
    
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
    
    amount_data_per_class = 300
    
    data_points = []
    for c in data_class:
        data_points = data_points + [DataPoint.DataPoint(_.text, _.hashtags, c[1], dictionary) for _ in
                                     TSV_Getter(c[0]).get_all_tsv_objects(amount_data_per_class)]
    
    # gather the data points into a whole training data
    training_data = TrainingData.TrainingData(data_points)    
    
    # You can print the data if you wanna see it
    # training_data.print_data()
    
    # Show the features
    print training_data.get_feature_dictionary()
    # print training_data.get_label_vector()
    
    # Get the feature matrix of this data
    feat_matrix = np.array(training_data.get_feature_matrix())
    
    
    # Soooo, that's your training matrix and your training label
    x = feat_matrix
    t = np.array(training_data.get_label_vector())
    
    size_all = x.shape[0]
    
    indices = list(range(x.shape[0]))
    random_indices = random.sample(indices, size_all/2)
    rest_indices = [index for index in indices if index not in random_indices] 
    
    #print 'all', indices
    #print 'random', random_indices
    #print 'rest', rest_indices   
    
    
    # Devide the data into train and test data (do it in a smarter way in the feature :D)
    x_train = x[random_indices]
    t_train = t[random_indices]
    x_test = x[rest_indices]
    t_test = t[rest_indices]
    
    # These are the parameters - #of features in the hidden layer, #of iterations to perform and #of classes and features
    L = 2;
    N = 50;
    number_classes = 2
    number_features = x_train.shape[1]
    
    
    #start with really small initial weights!!
    w = np.random.randn(L, number_classes)*0.015; 
    b = np.random.randn(number_classes)*0.0015; 
    v = np.random.randn(number_features, L)*0.015;
    a = np.random.randn(L)*0.0015; 
    
    print 'WWWWWWWWWWWWWWWWWW', w
    
    
    # So we learn the parameters
    w, b, v, a = mlp_train_set(w, b, v, a, N, L, x_train, t_train, number_classes, number_features);
    
    print 'WWWWWWWWWWWWWWWWWW', w
    
    # And then we use them to test
    cnt, cntall = count_correct_results(w, b, v, a, x_test, t_test);
    print 'cnt: ', cnt, '\n cntall: ', cntall
    
    
    
'''
Just saving some weights here for test purposes :P 
0015 and 015
WWWWWWWWWWWWWWWWWW [[ 0.03680083 -0.01718052]
 [ 0.01356237  0.0149547 ]
 [ 0.00702975 -0.00297079]]
WWWWWWWWWWWWWWWWWW [[-0.70942263  0.72904294]
 [-0.25232536  0.28084243]
 [-0.36663171  0.37069068]]
 
0025 and 025
 WWWWWWWWWWWWWWWWWW [[-0.00974345  0.0010707 ]
 [-0.00587517  0.00974238]
 [-0.02237335  0.03998623]]
WWWWWWWWWWWWWWWWWW [[-0.63406381  0.62539106]
 [ 0.21843463 -0.21456742]
 [-0.90502857  0.92264145]]
 
025 and 25
WWWWWWWWWWWWWWWWWW [[-0.19491818 -0.20358173]
 [ 0.01205856  0.12002121]
 [-0.15401177 -0.25199409]]
WWWWWWWWWWWWWWWWWW [[ 0.65981482 -1.05831473]
 [ 0.54044648 -0.4083667 ]
 [-1.11662407  0.7106182 ]]
 
 WWWWWWWWWWWWWWWWWW [[ 0.04358235  0.02683832]
 [-0.20655984 -0.14810111]
 [ 0.11560181  0.28404154]]
WWWWWWWWWWWWWWWWWW [[ 0.40703629 -0.33661561]
 [-1.18129089  0.82662993]
 [ 0.84203249 -0.44238913]]


'''