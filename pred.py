import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, CuDNNLSTM
import gaussian_nll as gauss
from keras import losses
from model_run import model

def predictionList(model, predLen):
    predList = []

    #predict(self, x, batch_size=32, verbose=0)
    for _ in range(predLen):
        predList.append(model.predict())

    return predList


