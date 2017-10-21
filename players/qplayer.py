from player import Player
import numpy as np
import random
from othello.qnetwork import QNetwork
from othello.experience_replay import ExperienceBuffer

class QPlayer(Player):

    def __init__(self,tile,train=False):
        Player.__init__(self,tile,train)

        self.QN = QNetwork()
        self.targetQN = QNetwork()
        self.myBuffer = ExperienceBuffer()
        self.gameBuffer = ExperienceBuffer()
        self.e = 1
        self.sess = None
        self.num_episodes = 1
        self.train = train

    def setSessionEpisodes(self,sess,num_episodes):
        """ Update player tf session
        @param tfSession sess
        """
        self.sess = sess
        self.num_episodes = num_episodes
        self.QN.pre_train_steps = num_episodes * 25
        self.targetQN.pre_train_steps = num_episodes * 25

    def setTrain(self,train):
        """ Update if player trains
        @param bool train
        """
        self.train = train

    def endGame(self):
        """ Update e greedy and game buffer """
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
        if np.random.rand(1) < self.e or total_steps < self.QN.pre_train_steps:
            action = random.choice(possibleMoves)
        else:
            Q = self.QN.getQout(s,self.sess)
            action = self.get_best_possible_action(possibleMoves,Q)
        if self.train:
            #Get new state and reward from environment and update
            sPrime,r,d = s.next(self.tile,action)
            self.gameBuffer.add(np.reshape(np.array([s.get1DBoard(),action,r,sPrime.get1DBoard(),d]),[1,5]))
            self.QN.update(total_steps,self.targetQN,self.myBuffer,self.sess)
        return action

    def get_best_possible_action(self,possible_moves,moves):
        """
        Get the bes possible move from a list
        @param list(int) possible_moves
        @param list(int) moves
        @return int move
        """
        sorted_moves = [(val,i) for i,val in enumerate(possible_moves)]
        sorted_moves.sort(key = lambda x: x[0], reverse = True)
        for move in sorted_moves:
            if move[0] in possible_moves:
                return move[0]
        return -1
