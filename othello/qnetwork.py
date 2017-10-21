import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
from experience_replay import updateTarget
from experience_replay import updateTargetGraph

class QNetwork(object):
    def __init__(self,lr=0.01):
        # Set learning parameters
        self.y = 0.99
        self.batch_size = 32 #Size of training batch
        self.pre_train_steps = 2500 #Number of steps used before training updates begin.
        tau = 0.001 #Amount to update target network at each step.
        trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(trainables,tau)

        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape=[None,64],dtype=tf.float32)
        hidden = slim.fully_connected(self.inputLayer,64,activation_fn=tf.nn.tanh,biases_initializer=None)
        self.Qout = slim.fully_connected(hidden,64,activation_fn=None,biases_initializer=None)
        self.predict = tf.argmax(self.Qout,1) #Get the best value

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[None],dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None],dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions,64,dtype=tf.float32)
        self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), reduction_indices=1)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        trainer = tf.train.GradientDescentOptimizer(lr)
        self.updateModel = trainer.minimize(self.loss)

    def getQout(self,s,sess):
        """ Return Q-values for the QPlayer
        @param board s
        @param tfSession sess
        @return list(float) Qout
        """
        return sess.run(self.Qout,feed_dict={self.inputLayer:[s.get1DBoard()]})

    def update(self,total_steps,targetQN,bufferP,sess):
        """ Update Networks with the experience buffer
        @param int total_steps
        @param QNetwork targetQN
        @param ExperienceBuffer bufferP
        @param tfSession sess
        """
        if total_steps > self.pre_train_steps and total_steps % 5 == 0:
            #We use Double-DQN training algorithm
            trainBatch = bufferP.sample(self.batch_size)
            Q1 = sess.run(self.predict,feed_dict={self.inputLayer:np.vstack(trainBatch[:,3])})
            Q2 = sess.run(targetQN.Qout,feed_dict={targetQN.inputLayer:np.vstack(trainBatch[:,3])})
            end_multiplier = -(trainBatch[:,4] - 1)
            doubleQ = Q2[range(self.batch_size),Q1]
            targetQ = trainBatch[:,2] + (self.y*doubleQ * end_multiplier)
            _ = sess.run(self.updateModel,feed_dict={self.inputLayer:np.vstack(trainBatch[:,0]),self.nextQ:targetQ,self.actions:trainBatch[:,1]})
            updateTarget(self.targetOps,sess)
