from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:100:64       Sigmoide
LOSS = 'mse'

class QNetworkSigmoid(QNetwork):
    def __init__(self,lr=0.05):
        QNetwork.__init__(self)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
        sgd = SGD(lr)
        self.model.compile(loss=LOSS,optimizer=sgd)
        print "Model generated"

    def getInputShape(self):
        return 64

    def getType(self):
        return "sigmoid"
