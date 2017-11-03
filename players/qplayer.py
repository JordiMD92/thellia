from player import Player
import numpy as np
import random
from othello.experience_replay import ExperienceBuffer

class QPlayer(Player):

    def __init__(self,tile,QN):
        Player.__init__(self,tile)

        self.QN = QN
        self.myBuffer = ExperienceBuffer()
        self.gameBuffer = ExperienceBuffer()
        self.e = 1
        self.sess = None
        self.num_episodes = 1
        self.pre_train_steps = 25

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
        if np.random.rand(1) < self.e or total_steps < self.pre_train_steps:
            action = random.choice(possibleMoves)
        else:
            Q = self.QN.getQout(s,self.tile,self.sess)
            action = self.get_best_possible_action(possibleMoves,Q)

        #Get new state and reward from environment and update
        sPrime,r,d = s.next(self.tile,action)
        if self.QN.getInputShape() == 64:
            sBoard = s.get1DBoard()
            sPrimeBoard = sPrime.get1DBoard()
        else:
            sBoard = s.get129Board(self.tile)
            sPrimeBoard = sPrime.get129Board(self.tile)
        self.gameBuffer.add(np.reshape(np.array([sBoard,action,r,sPrimeBoard,d]),[1,5]))
        if total_steps > self.pre_train_steps and total_steps % 5 == 0:
            self.QN.update(self.myBuffer,self.sess)
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
