from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.optimizers import SGD

#64:200:190:180...:64 RELU

LOSS = 'mse'

class QNetworkRelu(object):
    def __init__(self,lr=0.01):
        self.modelLoaded = False

        self.model = Sequential()

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
        self.model.add(Dropout(0.4))
        sgd = SGD(lr=0.01)
        self.model.compile(loss=LOSS,optimizer=sgd)

        print "Model generated"

    def get_model(self):
        return self.model

    def load_model(self,folder):
        self.model = load_model(folder+"/my_model.h5")
        self.modelLoaded = True
        print "Model loaded"

    def save_model(self,folder):
        self.model.save(folder+"/my_model.h5")
        print "Model saved"

    def getInputShape(self):
        return 64

    def isModelLoaded(self):
        return self.modelLoaded
