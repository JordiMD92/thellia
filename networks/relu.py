from qnetwork import QNetwork
import tensorflow as tf

#64:200:150:100:64      RELU
def_lr = 0.00025
def_drop = 0.4

class QNetworkRelu(QNetwork):
    def __init__(self,lr,drop):
        self.lr = def_lr if lr == 0 else lr
        self.drop =  def_drop if drop == 0 else drop
        QNetwork.__init__(self)

        self.inputLayer = tf.placeholder(shape=[None,64], dtype=tf.float32)
        hidden = tf.layers.dense(self.inputLayer, 200, activation=tf.nn.relu)
        hidden = tf.layers.dense(hidden, 150, activation=tf.nn.relu)
        hidden = tf.layers.dense(hidden, 100, activation=tf.nn.relu)
        dropLayer = tf.nn.dropout(hidden, drop)
	self.Qout = tf.layers.dense(inputs=dropLayer, units=64)
        self.predict = tf.argmax(self.Qout, 1)

        self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        self.actions_onehot = tf.one_hot(self.actions, 64, dtype=tf.float32)
        self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), reduction_indices=1)

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[None], dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        #optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        optimizer = tf.train.AdamOptimizer(learning_rate=lr)
        self.updateModel = optimizer.minimize(self.loss)

        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "relu"

    def getDrop(self):
        """ Returns dropout
        @return float drop
        """
        return self.drop
