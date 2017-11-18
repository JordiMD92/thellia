from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.optimizers import SGD

#64:200:190:180...:64 RELU
LOSS = 'mse'

class QNetworkRelu(QNetwork):
    def __init__(self,lr=0.01,drop=0.4):
        QNetwork.__init__(self)
        self.model.add(Dense(units=200,activation='relu',input_shape=(64,)))
        self.model.add(Dense(units=190,activation='relu'))
        self.model.add(Dense(units=180,activation='relu'))
        self.model.add(Dense(units=170,activation='relu'))
        self.model.add(Dense(units=160,activation='relu'))
        self.model.add(Dense(units=150,activation='relu'))
        self.model.add(Dense(units=140,activation='relu'))
        self.model.add(Dense(units=130,activation='relu'))
        self.model.add(Dense(units=120,activation='relu'))
        self.model.add(Dense(units=110,activation='relu'))
        self.model.add(Dense(units=100,activation='relu'))
        self.model.add(Dense(units=90,activation='relu'))
        self.model.add(Dense(units=80,activation='relu'))
        self.model.add(Dense(units=64,activation='relu'))
        self.model.add(Dropout(drop))
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
        return "relu"
