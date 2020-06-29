

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import gaussian_nll as gauss
from keras import losses

from NN_preprocessing import new_preprocessing as prep
import numpy as np
import pdb
import pprint as pp
from NN_preprocessing import options

from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint
import time
#import pred


def predictionList(model, predLen, division):
    predList = []
    sequence = []
    #predict(self, x, batch_size=32, verbose=0)
    x = [prep.randomSeq(division)]
    x = np.array(x)
    for _ in range(predLen):
        #breakpoint()
        y = model.predict(x)
        y = y[0][-1].tolist()
        x = x.tolist()
        predList.append(y)
        x = [x[0][1::]]
        x[0].append(y)
        x = np.array(x)

    return predList





d_cell_num = 7

main_path = './music_long/'
all_path = './music_all/'
validation_path = './music_long/validation/'

#main_path = all_path[:-14:]
#validation_path = [-14::]

#main_path = './s_subset/main/'
#all_path = './s_subset/'
#rel_path = './music_lowLen/'
#validation_path = './s_subset/validation/'
#scores = prep.loadScores(main_path)
#validation_scores = prep.loadScores(validation_path)
all_scores = prep.loadScores(all_path)

scores = all_scores[:-14:]
validation_scores = all_scores[-14::]

i ,o = prep.make_food(scores)
val_i, val_o = prep.make_food(validation_scores)

division = prep.normalisation_division(all_scores)
#val_division = prep.normalisation_division(validation_scores)

i = prep.normalise_food(i,division)
o = prep.normalise_out(o,division)
val_i = prep.normalise_food(val_i,division)
val_o = prep.normalise_out(val_o,division)

# is it OK that it has different normalisations ? Probaly NOT !!!

i = np.array(i)
o = np.array(o)
val_i = np.array(val_i)
val_o = np.array(val_o)
print(val_i.shape)
print(i.shape)

if options.binary:
    d_cell_num = 140
    i = np.reshape(i, (len(scores)*20,100,140))
    o = np.reshape(o, (len(scores)*20,100,140))

    val_i = np.reshape(val_i, (len(validation_scores)*20,100,140))
    val_o = np.reshape(val_o, (len(validation_scores)*20,100,140))

in_sh = i.shape
LSTM_activation = "tanh"

model = Sequential()
model.add(LSTM(70, input_shape=in_sh[1:], activation=LSTM_activation, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(128,activation=LSTM_activation, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(128,activation=LSTM_activation, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(128,activation=LSTM_activation, return_sequences=False))
model.add(Dropout(0.2))

model.add(Dense(d_cell_num,activation='softmax')) # >>> odpowiada za ostatni shape.

f_loss = 'categorical_crossentropy'
opt = tf.keras.optimizers.Adam(lr=1e-7, decay=1e-8)

model.compile(loss=f_loss,     # gauss.gaussian_nll
              optimizer = opt,
              metrics = ['accuracy'])
NAME = f'Model_{int(time.time())}'
tensorboard = TensorBoard(log_dir=f'logs/{NAME}')
chp_path = "RNN_Checkpoint-{epoch:02d}-{val_acc:.3f}"
#    checkpoint = ModelCheckpoint(f"models/{chp_path}.model",monitor='val_acc', verbose=1, save_best_only=True, mode='max')
checkpoint = ModelCheckpoint("models/{}.model".format(chp_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')) # saves only the best ones
if __name__ == "__main__":

    history=model.fit(i, o, batch_size=2, epochs=100,
              callbacks=[tensorboard,checkpoint],
                    validation_data=(val_i,val_o))
    predList = predictionList(model, 500, division)
