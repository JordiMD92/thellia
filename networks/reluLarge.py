from qnetwork import QNetwork
import tensorflow as tf

#64:200:180:160:140:120:100:80:64      RELU
def_lr = 0.0001
def_drop = 0.4

class QNetworkReluLarge(QNetwork):
    def __init__(self,lr,drop):
        self.lr = def_lr if lr == 0 else lr
        self.drop =  def_drop if drop == 0 else drop
        QNetwork.__init__(self)

        with tf.name_scope('inputLayer') as scope:
            self.inputLayer = tf.placeholder(shape=[None,64], dtype=tf.float32)
        with tf.name_scope('hidden200') as scope:
            hidden = tf.layers.dense(self.inputLayer, 200, activation=tf.nn.relu)
        with tf.name_scope('hidden180') as scope:
            hidden = tf.layers.dense(hidden, 180, activation=tf.nn.relu)
        with tf.name_scope('hidden160') as scope:
            hidden = tf.layers.dense(hidden, 160, activation=tf.nn.relu)
        with tf.name_scope('hidden140') as scope:
            hidden = tf.layers.dense(hidden, 140, activation=tf.nn.relu)
        with tf.name_scope('hidden120') as scope:
            hidden = tf.layers.dense(hidden, 120, activation=tf.nn.relu)
        with tf.name_scope('hidden100') as scope:
            hidden = tf.layers.dense(hidden, 100, activation=tf.nn.relu)
        with tf.name_scope('hidden80') as scope:
            hidden = tf.layers.dense(hidden, 80, activation=tf.nn.relu)
        with tf.name_scope('dropLayer') as scope:
            dropLayer = tf.nn.dropout(hidden, self.drop)
        with tf.name_scope('Qout') as scope:
            lastLayer = tf.layers.dense(inputs=dropLayer, units=64)
            #self.Qout = lastLayer

        with tf.name_scope('dueling') as scope:
            streamA, streamV = tf.split(lastLayer,2,1)
            xavier_init = tf.contrib.layers.xavier_initializer()
            AW = tf.Variable(xavier_init([64/2, 64]))
            VW = tf.Variable(xavier_init([64/2, 1]))
            advantage = tf.matmul(streamA, AW)
            value = tf.matmul(streamV, VW)

        with tf.name_scope('DuelingQout') as scope:
            self.Qout = value + tf.subtract(advantage,tf.reduce_mean(advantage,axis=1,keep_dims=True))

        with tf.name_scope('predict') as scope:
            self.predict = tf.argmax(self.Qout, 1)

        with tf.name_scope('actions') as scope:
            self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
        with tf.name_scope('actionsOH') as scope:
            self.actions_onehot = tf.one_hot(self.actions, 64, dtype=tf.float32)
        with tf.name_scope('Q') as scope:
            self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), reduction_indices=1)

        #Obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        with tf.name_scope('nextQ') as scope:
            self.nextQ = tf.placeholder(shape=[None], dtype=tf.float32)
        with tf.name_scope('loss') as scope:
            self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Q))
        #optimizer = tf.train.GradientDescentOptimizer(learning_rate=lr)
        with tf.name_scope('optimizer') as scope:
            optimizer = tf.train.AdamOptimizer(learning_rate=self.lr)
        with tf.name_scope('updateModel') as scope:
            self.updateModel = optimizer.minimize(self.loss)

        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "reluLargeDuel"

    def getDrop(self):
        """ Returns dropout
        @return float drop
        """
        return self.drop
