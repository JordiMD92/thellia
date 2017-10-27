import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

"""
128+1:200:150:100:64    Sigmoide
"""
class QNetwork129(object):
    def __init__(self,lr=0.01):
        # Set learning parameters
        self.y = 0.99
        self.batch_size = 32 #Size of training batch
        tau = 0.001 #Amount to update target network at each step.
        trainables = tf.trainable_variables()
        self.targetOps = self.updateTargetGraph(trainables,tau)

        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape=[None,129],dtype=tf.float32)
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
        return 129

    def getQout(self,s,tile,sess):
        """ Return Q-values for the QPlayer
        @param board s
        @param tfSession sess
        @return list(float) Qout
        """
        input129Node = s.get129Board(tile)
        return sess.run(self.Qout,feed_dict={self.inputLayer:[input129Node]})

    def update(self,bufferP,sess):
        """ Update Networks with the experience buffer
        @param ExperienceBuffer bufferP
        @param tfSession sess
        """
        trainBatch = bufferP.sample(self.batch_size)
        targetQ = sess.run(self.Qout,feed_dict={self.inputLayer:np.vstack(trainBatch[:,3])})
        maxQ1 = np.array(map(max,targetQ))
        reward = trainBatch[:,2] + self.y*maxQ1
        for idx in range(self.batch_size):
            targetQ[idx,trainBatch[idx,1]] = trainBatch[idx,2] + self.y*maxQ1[idx]
        _ = sess.run(self.updateModel,feed_dict={self.inputLayer:np.vstack(trainBatch[:,0]),self.nextQ:targetQ})

        self.updateTarget(self.targetOps,sess)

    def updateTargetGraph(self,tfVars,tau):
        total_vars = len(tfVars)
        op_holder = []
        for idx,var in enumerate(tfVars[0:total_vars//2]):
            op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
        return op_holder

    def updateTarget(self,op_holder,sess):
        for op in op_holder:
            sess.run(op)
