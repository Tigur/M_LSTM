import NN_preprocessing.new_preprocessing as prep
#from tensorflow.keras.models import Sequential
import tensorflow as tf

load_path = 'models/RNN_Checkpoint-300-0.888.model'
model = tf.keras.models.load_model(load_path)
init_info = prep.obtain_init()
prediction = model.predict(init_info)

print(prediction[1])
