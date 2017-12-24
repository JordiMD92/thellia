from qnetwork import QNetwork
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.optimizers import SGD, Adam

#64:200:190:180...:64 RELU
LOSS = 'mse'

def_lr = 0.005
def_drop = 0.4

class QNetworkReluSM(QNetwork):
    def __init__(self,lr,drop):
        self.lr = def_lr if lr == 0 else lr
        self.drop =  def_drop if drop == 0 else drop
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
        self.model.add(Dense(units=64,activation='softmax'))
        #optimizer = SGD(lr)
        optimizer = Adam(lr=lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        self.model.compile(loss=LOSS,optimizer=optmizer)
        print "Model ["+self.getType()+"] generated"

    @classmethod
    def getType(self):
        """ Returns Network type
        @return string type
        """
        return "reluSM"

    def getDrop(self):
        """ Returns dropout
        @return float drop
        """
        return self.drop
