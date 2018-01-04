from player import Player
import numpy as np
import random
import tensorflow as tf

class QPlayer(Player):

    def __init__(self,tile,QN,targetQN,mode,num_episodes,train):
        Player.__init__(self,tile=tile)
        self.QN = QN
        self.targetQN = targetQN
        self.mode = mode
        self.num_episodes = num_episodes
        self.train = train
        self.e = 1
        if QN.isModelLoaded():
            self.e = 0.1
        self.y = 0.99
        self.conta = 0
        self.updateFreq = 8

    def updateEpsilon(self):
        """ Update e greedy """
        if self.e > 0.01:
            self.e -= (0.9/self.num_episodes)

    def getMove(self,game,board,possibleMoves):
        """ Get the player's move
        @param board board
        @param list(int) possibleMoves
        @return int action
        """
        s = board.getBoardState(self.tile)
        move_mask = np.zeros((64), dtype='float32')
        move_mask[possibleMoves] = 1
        #Choose move e-greedyly, random or from network
        if np.random.rand(1) < self.e and self.mode == "train":
            action = random.choice(possibleMoves)
        else:
            action = self.sess.run(self.QN.predict, feed_dict={self.QN.inputLayer:[s],self.QN.move_mask:[move_mask]})
            action = action[0]
        self.conta += 1

        if self.mode != "play" and self.train: #mode == "train" or mode == "load"
            #Get new state and reward from environment and update
            sPrime,r,done,move_maskPrime = game.next(board,action,self.tile)
            self.QN.addExperience(s,action,r,sPrime,done,move_mask,move_maskPrime)
            #Train when mem if it's len is at least batch_size
            if self.conta % self.updateFreq == 0 and self.conta >= self.QN.batch_size:
                trainBatch = self.QN.sample()
                #s_batch,a_batch,r_batch,sP_batch,d_batch,move_mask = trainBatch[i]
                Q1 = self.sess.run(self.QN.predict,feed_dict={self.QN.inputLayer:np.vstack(trainBatch[:,3]),self.QN.move_mask:np.vstack(trainBatch[:,6])})
                Q2 = self.sess.run(self.targetQN.Qout,feed_dict={self.targetQN.inputLayer:np.vstack(trainBatch[:,3]),self.targetQN.move_mask:np.vstack(trainBatch[:,6])})
                end_multiplier = -(trainBatch[:,4] - 1)
                doubleQ = Q2[range(self.QN.batch_size),Q1]
                targetQ = trainBatch[:,2] + (self.y*doubleQ*end_multiplier)
                _,loss = self.sess.run([self.QN.updateModel,self.QN.loss],feed_dict={self.QN.inputLayer:np.vstack(trainBatch[:,0]),self.QN.move_mask:np.vstack(trainBatch[:,5]),self.QN.nextQ:targetQ,self.QN.actions:trainBatch[:,1]})
                self.QN.updateTarget(self.targetOps,self.sess)

                summary = tf.Summary(value=[tf.Summary.Value(tag="loss",simple_value=loss),])
                self.QN.tbWriter.add_summary(summary)
            if done:
                self.updateEpsilon()
        return action
        
    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "QP"
