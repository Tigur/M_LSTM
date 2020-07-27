import numpy
from keras import backend as K
import tensorflow as tf

tf.enable_eager_execution()

def classClippingLoss(y_true,y_pred):
    loss = 0
    #with tf.Session() as sess:
     #   y_trueL = y_true.eval()
      #  y_predL = y_pred.eval()
    for index in range(7):
        if index == 2:
            if not y_pred[index] == y_true[index]:
                loss = loss + 200 # VERY ARGUABLE SOLUTION !!
        else:
            loss = loss + K.sqrt(K.mean(K.square(y_pred[index] - y_true[index])))

    return loss
