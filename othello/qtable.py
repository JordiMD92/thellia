import gym
import numpy as np
import random
import board
from players.qplayer import QPlayer
import copy

class QTable():
    def __init__(self,tile,secondPlayer):
        self.black = QPlayer(tile)
        self.white = secondPlayer

        self.Q = np.zeros([64,64])

        # Set learning parameters
        self.y = 0.99
        self.lr = .8
        self.num_episodes = 50
        self.rList = []

    def run(self):
        for i in range(self.num_episodes):
            #Reset environment and get first new observation
            s = board.Board()
            rAll = 0
            actualTurnPlayer = self.black
            passCount = 0
            #The Q-Table learning algorithm
            while s.getRemainingPieces() > 0 and passCount < 2:
                if actualTurnPlayer == self.white:
                    c,r = actualTurnPlayer.getMove(s)
                    if c != -1 or r != -1:
                        s.updateBoard(actualTurnPlayer.getTile(),c,r)
                        passCount = 0
                    else:
                        passCount += 1
                else:
                    possible_actions = actualTurnPlayer.checkMoves(s);
                    if possible_actions:
                        passCount = 0
                        pos = list(random.choice(possible_actions))
                        #Choose an action by greedily (with noise) picking from Q table
                        a = np.argmax(self.Q[s.get1DBoard(),:] + np.random.randn(1,64)*(1./(i+1)))
                        pos[0] , pos[1] = a // 8 , a % 8
                        #Get new state and reward from environment
                        sPrime,r = self.get_next_state(actualTurnPlayer.getTile(),pos,copy.deepcopy(s))
                        #Update Q-Table with new knowledge
                        self.Q[s.get1DBoard(),a] = self.Q[s.get1DBoard(),a] + self.lr*(r + self.y*np.max(self.Q[sPrime.get1DBoard(),:]) - self.Q[s.get1DBoard(),a])
                        if r == -1:
                            continue
                        else:
                            rAll += r
                            s = sPrime
                    else:
                        passCount += 1
                #Next turn
                actualTurnPlayer = self.white if actualTurnPlayer is self.black else self.black
            self.rList.append(rAll)

        print "Score over time: " +  str(sum(self.rList)/self.num_episodes)

        print "Final Q-Table Values"
        print self.Q

    """ Update board and return reward """
    def get_next_state(self,tile,pos,s):
        if s.updateBoard(tile,pos[0],pos[1]):
            r=1
        else:
            r=-1
        return s,r

    #TODO delete this code
    def printBoard(self,board):
        """ Print actual board state """
        print("\n\n   A   B   C   D   E   F   G   H  ")
        print(" - - - - - - - - - - - - - - - - -")
        for r in range(0,8,1):
            row = ""
            for c in range(0,8,1):
                value = "|   "
                if board[c][r] == -1: value = "| X "
                if board[c][r] == 1: value = "| O "
                row = row+value
            print(str(r+1)+row+"|")
            print(" - - - - - - - - - - - - - - - - -")
