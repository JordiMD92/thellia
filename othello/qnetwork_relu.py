import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

"""
64:200:190:180...:64 RELU
"""
class QNetworkRelu(object):
    def __init__(self,lr=0.001):
        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape=[None,64],dtype=tf.float32)
        hidden = tf.layers.dense(self.inputLayer, 200, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 190, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 180, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 170, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 160, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 150, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 140, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 130, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 120, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 110, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 100, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 90, activation = tf.nn.relu)
        hidden = tf.layers.dense(hidden, 80, activation = tf.nn.relu)
        # Dropout
        dropout = tf.layers.dropout(hidden, rate=0.4)
        # Qout Layer
        self.Qout = tf.layers.dense(inputs=dropout, units=64)
        self.predict = tf.argmax(self.Qout,1) #Get the best value

        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,64,dtype=tf.float32)
        self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), reduction_indices=1)

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        trainer = tf.train.GradientDescentOptimizer(lr)
        self.updateModel = trainer.minimize(self.loss)

    def getInputShape(self):
        return 64
