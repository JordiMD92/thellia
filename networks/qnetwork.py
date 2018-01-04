from collections import deque
import numpy as np
import random

batch_size = 32

class QNetwork:
    def __init__(self):
        self.modelLoaded = False
        self.memBuffer = deque(maxlen=50000)
        self.batch_size = batch_size

    def getModel(self):
        """ Return QN model
        @return Keras.model model
        """
        return self.model

    def initTensorboard(self,tbWriter):
        self.tbWriter = tbWriter

    def loadModel(self):
        """ Load model_name to QN
        @param String folder
        """
        self.modelLoaded = True

    def isModelLoaded(self):
        return self.modelLoaded

    def getLR(self):
        """ Returns learning rate
        @return float lr
        """
        return self.lr

    def addExperience(self,s,action,r,sPrime,done,move_mask,move_maskPrime):
        """ Add experience to the memory
        @param Board s
        @param int action
        @param int r
        @param Board sPrime
        @param bool done
        @param list[] move_mask
        """
        self.memBuffer.append((s,action,r,sPrime,done,move_mask,move_maskPrime))

    def sample(self):
        """ Return batch of experiences
        @return array[batch_size][s,action,r,sPrime,done]
        """
        return np.reshape(np.array(random.sample(self.memBuffer, batch_size)),[batch_size,7])

    def updateTargetGraph(self,tfVars,tau):
        total_vars = len(tfVars)
        op_holder = []
        for idx,var in enumerate(tfVars[0:total_vars//2]):
            op_holder.append(tfVars[idx+total_vars//2].assign((var.value()*tau) + ((1-tau)*tfVars[idx+total_vars//2].value())))
        return op_holder

    def updateTarget(self,op_holder,sess):
        for op in op_holder:
            sess.run(op)
