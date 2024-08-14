import csv
import math
import numpy as np
import pandas as pd

rg = np.random.default_rng()

def Integrate_Data():
    with open('data.txt', 'r') as data:
        data = csv.reader(data)


def Generate_Data(n_features, n_values):
    features = rg.random((n_features, n_values))
    #print('Features:',features)
    weights = rg.random((1, n_values))[0]
    #print('\nWeights:',weights)
    targets = np.random.choice([0,1,2], n_features)
    #print('\nTargets:',targets)
    data = pd.DataFrame(features, columns=[[('x' + str(i)) for i in range(len(features[0]))]])
    data['targets'] = targets

    return data, weights
def Get_Weighted_Sum(feature, weights, bias):
    return np.dot(feature, weights) + bias

def Sigmoid(w_sum):
    return 1/(1+np.exp(-w_sum))

def Activation_ReLU(w_sum):
    return np.maximum(0.00001, w_sum)

def Cross_Entropy(target, prediction):
    #print(f'-({target}*np.log10({prediction}) + (1-{target})*np.log10(1-{prediction}))')
    return -(target*np.log10(prediction) + (1-target)*np.log10(1-prediction))

def Update_Weights(weights, l_rate, target, prediction, feature):
    new_weights = []
    for x,w in zip(feature,weights):
        new_w = w + l_rate*(target-prediction)*x
        new_weights.append(new_w)
    return new_weights

def Update_Bias(bias, l_rate, target, prediction):
    return bias + l_rate*(target-prediction)
