from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:100:64       Sigmoide
LOSS = 'mse'

def_lr = 0.05

class QNetworkSigmoid(QNetwork):
    def __init__(self,batch_size,lr):
        self.lr = def_lr if lr == 0 else lr
        QNetwork.__init__(self,batch_size)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
        sgd = SGD(lr)
        self.model.compile(loss=LOSS,optimizer=sgd)
        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "sigmoid"

    def getLR(self):
        """ Returns learning rate
        @return float lr
        """
        return self.lr
