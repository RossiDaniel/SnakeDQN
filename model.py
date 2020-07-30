import tensorflow as tf
from tensorflow import keras
import numpy as np
from collections import deque
import random

np.random.seed(42)

class DQM():
    def __init__(self,width,height,size_buffer=100000,update_term=2,batch_size = 25000, discount=0.5,equalize_term=2):
        self.width = width
        self.height = height

        self.train_model = self.create_graph()
        self.predict_model = self.create_graph()
        
        self.equalize_model()

        self.size_buffer = size_buffer
        self.buffer = deque(maxlen=size_buffer)
        self.update_counter = 0
        self.update_term = update_term
        self.batch_size = batch_size
        self.discout = discount
        self.model_path = "new_model.h5"

        self.equalize_counter = 0
        self.equalize_term = equalize_term

    def create_graph(self):
        model = keras.models.Sequential([
            keras.layers.InputLayer(input_shape=[self.width,self.height,1]),
            keras.layers.Conv2D(16,(3,3),activation="tanh"),
            keras.layers.Flatten(),
            keras.layers.Dense(128,activation="tanh"),
            keras.layers.Dense(64,activation="tanh"),
            keras.layers.Dense(32,activation="tanh"),
            keras.layers.Dense(4,activation="linear")
        ])
        model.compile(loss="mse", optimizer="adam", metrics=['mean_absolute_percentage_error'])
        return model
  
    def add_train_data(self, transition):
        self.buffer.append(transition)

    def train(self):
        if(len(self.buffer)<self.batch_size):return 
        batch = random.sample(self.buffer, min(len(self.buffer),self.batch_size))

        X_states = tf.convert_to_tensor(np.array([t[0] for t in batch]), np.float32)
        X_next_states = tf.convert_to_tensor(np.array([t[3] for t in batch]), np.float32)

        Y_current_q_values = self.train_model.predict(X_states)
        Y_future_q_values = self.predict_model.predict(X_next_states)
                
        for index, (current_state, action, reward, new_state, done) in enumerate(batch):
            if not done:
                max_future_q_value = np.max(Y_future_q_values[index])
                Y_current_q_values[index][action] = reward + self.discout * max_future_q_value
            else:
                Y_current_q_values[index] = reward
        
        Y_q_values = tf.convert_to_tensor(Y_current_q_values, np.float32)

        self.train_model.fit(x=X_states, y=Y_q_values, batch_size=min(len(self.buffer),self.batch_size),epochs=1, verbose=1)
        self.train_model.save_weights(self.model_path)
        self.equalize_counter += 1
        if self.equalize_counter == self.equalize_term:
            self.equalize_counter = 0
            self.equalize_model()
     
    def predict_q_values(self, state):
        X = np.array([state])
        X_tf = tf.convert_to_tensor(X, np.float32)
        return self.train_model.predict(X)

    def equalize_model(self):
        self.predict_model.set_weights(self.train_model.get_weights())

    def load_trained_model(self):
        self.train_model.load_weights(self.model_path)
        self.equalize_model()