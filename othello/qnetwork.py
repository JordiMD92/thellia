class QNetwork(object):
    def __init__(self,tf,lr):
        #These lines establish the feed-forward part of the network used to choose actions
        self.inputLayer = tf.placeholder(shape=[1,64],dtype=tf.float32)
        self.W = tf.Variable(tf.random_uniform([64,64],0,0.01))
        self.Qout = tf.matmul(self.inputLayer,self.W)
        #self.predict = tf.argmax(self.Qout,1) #Get the best value

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[1,64],dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        self.trainer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        self.updateModel = self.trainer.minimize(self.loss)
