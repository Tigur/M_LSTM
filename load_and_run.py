import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import gaussian_nll as gauss
from keras import losses


tf.enable_eager_execution()

from NN_preprocessing import new_preprocessing as prep
import numpy as np
import pdb
import pprint as pp
from NN_preprocessing import options

from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
import time
#import pred
from cost_fun import *
from argparse import ArgumentParser
from keras.models import load_model

parser = ArgumentParser()
parser.add_argument("-f","--file", dest="filename", default='current_sample.mid',
                    help="name of the output file", type=str)
parser.add_argument("-e","--epochs",dest="arg_epochs", default=100,
                    help="numebr of epochs", type=int)
parser.add_argument("--oLength", dest="o_len", default=100,
                    help="output song length",type=int)
parser.add_argument("--fragmentLen", dest="fragLen", default=20,
                    help="Length of each fragment",type=int)
parser.add_argument("--fragmentNum", dest="fragNum", default=20,
                    help="Number of fragments from one song",type=int)
parser.add_argument("-lr", dest="learning_rate", default=1e-4,
                    help="learning rate", type=float)
parser.add_argument("--decay",dest="decay",default=1e-5,
                    help="decay rate", type=float)

args = parser.parse_args()

fileName = './predicted/' + args.filename
options.fragment_len = args.fragLen
options.fragment_num = args.fragNum




def predictionList(model, predLen, division):
    predList = []
    sequence = []
    #predict(self, x, batch_size=32, verbose=0)
    x = [prep.randomSeq(division)]
    x = np.array(x)
    for _ in range(predLen):
        #breakpoint()
        y = model.predict(x)
        y = y[0].tolist()
        x = x.tolist()
        predList.append(y)
        x = [x[0][1::]]
        x[0].append(y)
        x = np.array(x)

    return predList


checkpoint_filepath = './models/RNN_Checkpoint-300-0.512.model'

model = load_model(checkpoint_filepath)

predList = predictionList(model, args.o_len, division)
predScore = prep.conv_to_music(predList,division)
fp = predScore.write('midi',fp=fileName)
