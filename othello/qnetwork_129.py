from tensorflow.python.keras.models import Sequential, model_from_json
from tensorflow.python.keras.layers import Dense


#128+1:200:150:100:64    Sigmoide

MODEL_PATH = 'models/'
LOSS = 'mse'
OPTIMIZER = 'sgd'

class QNetwork129(object):
    def __init__(self,lr=0.05):
        #TODO fix all this, compile with output 64, need input 129
        self.model = Sequential()

        self.model.add(Dense(units=200,activation='sigmoid',input_shape=(129,)))
        self.model.add(Dense(units=150,activation='sigmoid'))
        self.model.add(Dense(units=100,activation='sigmoid'))
        self.model.add(Dense(units=64,activation='sigmoid'))
        self.model.compile(loss=LOSS,optimizer=OPTIMIZER)

        print "Model generated"

    def get_model(self):
        return self.model

    def load_model(self):
        json = open(MODEL_PATH,'r').read()
        model = model_from_json(json)
        model.compile(loss=LOSS,optimizer=OPTIMIZER)

        print "Model loaded"
        return model

    def save_model(self,model):
        json = model.to_json()
        with open(MODEL_PATH,'w') as f:
            f.write(json)

        print "Model saved"

    def getInputShape(self):
        return 129
