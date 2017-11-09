import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from player import Player
import numpy as np
import random
from othello.experience_replay import ExperienceBuffer
from othello.experience_replay import updateTargetGraph
from othello.experience_replay import updateTarget


class QPlayer(Player):

    def __init__(self,tile,mainQN,targetQN):
        Player.__init__(self,tile)

        self.mainQN = mainQN
        self.targetQN = targetQN
        self.myBuffer = ExperienceBuffer()
        self.gameBuffer = ExperienceBuffer()
        self.e = 1
        self.sess = None
        self.num_episodes = 1
        self.pre_train_steps = 25
        self.y = 0.99
        self.batch_size = 32 #Size of training batch
        tau = 0.001 #Amount to update target network at each step.
        trainables = tf.trainable_variables()
        self.targetOps = updateTargetGraph(trainables,tau)

    def setSessionEpisodes(self,sess,num_episodes):
        """ Update player tf session
        @param tfSession sess
        """
        self.sess = sess
        self.num_episodes = num_episodes
        self.pre_train_steps = num_episodes * 25

    def endGame(self):
        """ Update e greedy and game buffer """
        if self.e > 0.01:
            self.e -= (0.9/self.num_episodes)
        self.myBuffer.add(self.gameBuffer.buffer)
        self.gameBuffer = ExperienceBuffer()

    def getMove(self,s,possibleMoves,total_steps):
        """ Get the player's move
        @param board s
        @param list(int) possibleMoves
        @param int total_steps
        @return int action
        """
        #Choose move e-greedyly, random or from network
        if self.mainQN.getInputShape() == 64:
            boardShape = s.get1DBoard()
        else:
            boardShape = s.get129Board(self.tile)
        Qout = self.sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[boardShape]})
        if np.random.rand(1) < self.e or total_steps < self.pre_train_steps:
            action = random.choice(possibleMoves)
        else:
            action = self.get_best_possible_action(possibleMoves,Qout)

        #Get new state and reward from environment and update
        sPrime,r,d = s.next(self.tile,action)
        if self.mainQN.getInputShape() == 64:
            sBoard = s.get1DBoard()
            sPrimeBoard = sPrime.get1DBoard()
        else:
            sBoard = s.get129Board(self.tile)
            sPrimeBoard = sPrime.get129Board(self.tile)
        self.gameBuffer.add(np.reshape(np.array([sBoard,action,r,sPrimeBoard,d]),[1,5]))
        if total_steps > self.pre_train_steps and total_steps % 5 == 0:
            #We use Double-DQN training algorithm
            trainBatch = self.myBuffer.sample(self.batch_size)
            Q1 = self.sess.run(self.mainQN.predict,feed_dict={self.mainQN.inputLayer:np.vstack(trainBatch[:,3])})
            Q2 = self.sess.run(self.targetQN.Qout,feed_dict={self.targetQN.inputLayer:np.vstack(trainBatch[:,3])})
            end_multiplier = -(trainBatch[:,4] - 1)
            doubleQ = Q2[range(self.batch_size),Q1]
            targetQ = trainBatch[:,2] + (self.y*doubleQ * end_multiplier)
            _ = self.sess.run(self.mainQN.updateModel,feed_dict={self.mainQN.inputLayer:np.vstack(trainBatch[:,0]),self.mainQN.nextQ:targetQ,self.mainQN.actions:trainBatch[:,1]})
            updateTarget(self.targetOps,self.sess)

        return action

    def get_best_possible_action(self,possible_moves,moves):
        """
        Get the bes possible move from a list
        @param list(int) possible_moves
        @param list(int) moves
        @return int move
        """
        sorted_moves = [(val,i) for i,val in enumerate(moves[0])]
        sorted_moves.sort(key = lambda x: x[0], reverse = True)
        for move in sorted_moves:
            if move[1] in possible_moves:
                return move[1]
        return -1
