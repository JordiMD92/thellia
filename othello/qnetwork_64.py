import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

"""
64:200:150:100:64       Sigmoide
"""
class QNetwork64(object):
    def __init__(self,lr=0.01):
        # Set learning parameters
        self.y = 0.99

        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape=[None,64],dtype=tf.float32)
        hidden = tf.layers.dense(self.inputLayer, 200, activation = tf.nn.sigmoid)
        hidden = tf.layers.dense(hidden, 150, activation = tf.nn.sigmoid)
        hidden = tf.layers.dense(hidden, 100, activation = tf.nn.sigmoid)
        self.Qout = tf.layers.dense(hidden,64,activation = tf.nn.sigmoid)
        self.predict = tf.argmax(self.Qout,1) #Get the best value

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[None,64],dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        trainer = tf.train.GradientDescentOptimizer(lr)
        self.updateModel = trainer.minimize(self.loss)

    def getInputShape(self):
        return 64

    def getQout(self,s,tile,sess):
        """ Return Q-values for the QPlayer
        @param board s
        @param tfSession sess
        @return list(float) Qout
        """
        return sess.run(self.Qout,feed_dict={self.inputLayer:np.identity(64)[s.get1DBoard()]})

    def update(self,Q,sBoard,action,r,sPrimeBoard,sess):
        """ Update Networks
        @param ExperienceBuffer bufferP
        @param tfSession sess
        """
        Q1 = sess.run(self.Qout,feed_dict={self.inputLayer:np.identity(64)[sPrimeBoard]})
        maxQ1 = np.max(Q1)
        targetQ = Q
        targetQ[0,action] = r + self.y*maxQ1
        _ = sess.run(self.updateModel,feed_dict={self.inputLayer:np.identity(64)[sBoard],self.nextQ:targetQ})
