from tensorflow.python.keras.models import Sequential, load_model

class QNetwork:
    def __init__(self):
        self.modelLoaded = False
        self.model = Sequential()

    def getModel(self):
        return self.model

    def loadModel(self,folder):
        self.model = load_model(folder+"/my_model.h5")
        self.modelLoaded = True

    def saveModel(self,folder):
        self.model.save(folder+"/my_model.h5")

    def isModelLoaded(self):
        return self.modelLoaded

    def getInputShape(self):
        pass

    def getType(self):
        pass
