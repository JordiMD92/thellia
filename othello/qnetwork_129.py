import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

"""
128+1:200:150:100:64    Sigmoide
"""
class QNetwork129(object):
    def __init__(self,lr=0.05):
        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape = [None,129], dtype = tf.float32)
        hidden = tf.layers.dense(self.inputLayer, 200, activation = tf.nn.sigmoid)
        hidden = tf.layers.dense(hidden, 150, activation = tf.nn.sigmoid)
        hidden = tf.layers.dense(hidden, 100, activation = tf.nn.sigmoid)
        self.Qout = tf.layers.dense(hidden, 64, activation = tf.nn.sigmoid)
        self.predict = tf.argmax(self.Qout,1) #Get the best value

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape = [None,64], dtype = tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        trainer = tf.train.GradientDescentOptimizer(lr)
        self.updateModel = trainer.minimize(self.loss)

    def getInputShape(self):
        return 129
