from tensorflow.python.keras.models import Sequential, load_model
import tensorflow as tf
from collections import deque
import random

batch_size = 32

class QNetwork:
    def __init__(self):
        self.modelLoaded = False
        self.model = Sequential()
        self.memBuffer = deque(maxlen=50000)
        self.batch_size = batch_size

    def getModel(self):
        """ Return QN model
        @return Keras.model model
        """
        return self.model

    def initTensorboard(self,folder):
        self.tbWriter = tf.summary.FileWriter(folder+'/Graph')

    def loadModel(self,folder):
        """ Load model_name to QN
        @param String folder
        """
        self.model = load_model(folder+"/my_model.h5")
        self.modelLoaded = True

    def saveModel(self,folder):
        """ Save model to folder name
        @param String folder
        """
        self.model.save(folder+"/my_model.h5")

    def isModelLoaded(self):
        return self.modelLoaded

    def getLR(self):
        """ Returns learning rate
        @return float lr
        """
        return self.lr

    def addExperience(self,s,action,r,sPrime,done):
        """ Add experience to the memory
        @param Board s
        @param int action
        @param int r
        @param Board sPrime
        @param bool done
        """
        self.memBuffer.append((s,action,r,sPrime,done))

    def sample(self):
        """ Return batch of experiences
        @return list[batch_size][s,action,r,sPrime,done]
        """
        return random.sample(self.memBuffer, batch_size)
