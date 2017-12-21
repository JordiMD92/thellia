from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:64       Softmax
LOSS = 'mse'

def_lr = 0.005

class QNetworkSigmoidSM(QNetwork):
    def __init__(self,lr):
        self.lr = def_lr if lr == 0 else lr
        QNetwork.__init__(self)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='softmax'))
        sgd = SGD(lr)
        self.model.compile(loss=LOSS,optimizer=sgd)
        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "sigmoidSM"
