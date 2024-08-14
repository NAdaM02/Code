import numpy as np
import pandas as pd
from functions import Integrate_Data, Generate_Data, Get_Weighted_Sum, Sigmoid, Activation_ReLU, Cross_Entropy, Update_Weights, Update_Bias
import matplotlib
import time

start_time = time.time()

bias = 0.5
l_rate = 0.000005
epochs = 1000
epoch_loss = []

data, weights = Generate_Data(50,100)


def Train_Model(data, weights, bias, l_rate, epochs):
    for e in range(epochs):
        individual_loss = []
        for i in range(len(data)):
            feature = data.loc[i][:-1]
            target = data.loc[i][-1]
            w_sum = Get_Weighted_Sum(feature, weights, bias)
            prediction = Sigmoid(w_sum) # / Activation_ReLU(w_sum)
            loss = Cross_Entropy(target, prediction)
            individual_loss.append(loss)
            # gradient descent
            weights = Update_Weights(weights, l_rate, target, prediction, feature)
            bias = Update_Bias(bias, l_rate, target, prediction)
        average_loss = sum(individual_loss)/len(individual_loss)
        epoch_loss.append(average_loss)
        elapsed_time = time.time()-start_time
        expected_time = elapsed_time*(epochs/(e+1))
        remaining_time = expected_time - elapsed_time
        print('\r',str(average_loss)[:6],'\t\t\t','.'*int(e/epochs*10),'_'*(10-int(e/epochs*10+1)),'\t\t\t(',str(e/epochs*100)[:4],'%)\t\t\tRemaining: ~',str(remaining_time)[:4],'s',end='',sep='')

Train_Model(data, weights, bias, l_rate, epochs)

# plotting average loss
df = pd.DataFrame(epoch_loss)
df_plot = df.plot(kind='line', grid=True).get_figure()
df_plot.savefig('Training_Loss.pdf')
open('Training_Loss.pdf')

elapsed_time = time.time()-start_time
print("\nElapsed time:  ", str(elapsed_time)[:5],'s',sep='')
