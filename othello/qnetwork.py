import tensorflow.contrib.slim as slim

class QNetwork(object):
    def __init__(self,tf,lr=0.01):
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
        loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        trainer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        self.updateModel = trainer.minimize(loss)
