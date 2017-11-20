from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:64       Softmax
LOSS = 'mse'

class QNetworkSoftmax(QNetwork):
    def __init__(self,batch_size,lr=0.05):
        QNetwork.__init__(self,batch_size)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='softmax'))
        sgd = SGD(lr)
        self.model.compile(loss=LOSS,optimizer=sgd)
        print "Model ["+self.getType()+"] generated"

    def getInputShape(self):
        """ Returns Network input shape
        @return int shape
        """
        return 64

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "softmax"
