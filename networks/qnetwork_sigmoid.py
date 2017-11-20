from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:100:64       Sigmoide
LOSS = 'mse'

class QNetworkSigmoid(QNetwork):
    def __init__(self,batch_size,lr=0.05):
        QNetwork.__init__(self,batch_size)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
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
        return "sigmoid"