from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import SGD

#64:200:150:100:64       Sigmoide

LOSS = 'mse'

class QNetwork64(object):
    def __init__(self,lr=0.05):
        self.modelLoaded = False

        self.model = Sequential()

        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(64,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
        sgd = SGD(lr=0.05)
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
