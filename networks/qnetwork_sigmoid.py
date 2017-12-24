from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD, Adam

#64:200:150:100:64       Sigmoide
LOSS = 'mse'

def_lr = 0.005

class QNetworkSigmoid(QNetwork):
    def __init__(self,lr):
        self.lr = def_lr if lr == 0 else lr
        QNetwork.__init__(self)
        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
        #optimizer = SGD(lr)
        optimizer = Adam(lr=lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        self.model.compile(loss=LOSS,optimizer=optmizer)
        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "sigmoid"
