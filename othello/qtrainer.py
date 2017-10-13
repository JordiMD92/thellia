from __future__ import division
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np
import random
import copy
import tensorflow as tf
import board
from qnetwork import QNetwork
from qplayer import QPlayer

class QTrainer():

    def __init__(self,tile,secondPlayer):
        tf.reset_default_graph()
        self.black = QPlayer(tile)
        self.white = secondPlayer
        self.mainQN = QNetwork()

        # Set learning parameters
        self.y = 0.99
        self.e = 1
        self.num_episodes = 10
        self.eDrop = 0.9 / self.num_episodes
        #create lists to contain total rewards
        self.rList = []

    def run(self):
        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            for i in range(self.num_episodes):
                #Reset enviorement and start new board
                s = board.Board()
                rAll = 0
                actualTurnPlayer = self.black
                passCount = 0
                #The Q-Network
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
                            #Choose an action by greedily (with e chance of random action) from the Q-network
                            a,Q = sess.run([self.mainQN.predict,self.mainQN.Qout],feed_dict={self.mainQN.inputLayer:[s.get1DBoard()]})
                            if np.random.rand(1) < self.e:
                                a[0] = pos[0]+pos[1]*8
                            else:
                                pos[0] , pos[1] = a[0] // 8 , a[0] % 8
                            #Get new state and reward from environment
                            sPrime,r = self.get_next_state(actualTurnPlayer.getTile(),pos,copy.deepcopy(s))
                            #Obtain the Q' values by feeding the new state through our network
                            QPrime = sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[sPrime.get1DBoard()]})
                            #Obtain maxQ' and set our target value for chosen action.
                            maxQPrime = np.max(QPrime)
                            targetQ = Q
                            targetQ[0,a[0]] = r + self.y*maxQPrime
                            #Train our network using target and predicted Q values
                            _ = sess.run([self.mainQN.updateModel,self.mainQN.W],feed_dict={self.mainQN.inputLayer:[s.get1DBoard()],self.mainQN.nextQ:targetQ})
                            #If Qplayer made bad move -> repeat, else next state
                            if r == -1:
                                continue
                            else:
                                rAll += r
                                s = sPrime
                        else:
                            passCount += 1
                    #Next turn
                    actualTurnPlayer = self.white if actualTurnPlayer is self.black else self.black
                #End Game: Reduce chance of random action as we train the model.
                self.e -= self.eDrop
                self.jList.append(j)
                self.rList.append(rAll)

                #self.printBoard(s.getBoard())
                #print "egreedy: " + str(self.e)
                print "(i) "+str(i)+" - Score " +str(s.getScore())
        print("Percent of succesful episodes: " + str(sum(self.rList)/self.num_episodes) + "%")

    """ Update board and return reward """
    def get_next_state(self,tile,pos,s):
        if s.updateBoard(tile,pos[0],pos[1]):
            r=1
        else:
            r=-1
        return s,r


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
