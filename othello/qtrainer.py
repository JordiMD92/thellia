from __future__ import division
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np
import random
import copy
import tensorflow as tf
import board
from qnetwork import QNetwork
from players.qplayer import QPlayer

class QTrainer():

    def __init__(self,tile,secondPlayer,view):
        # Set learning parameters
        self.num_episodes = 100
        self.lr = 0.03
        self.y = 0.99
        self.e = 1
        self.eDrop = 0.9 / self.num_episodes
        #create lists to contain total rewards
        #self.rList = []

        tf.reset_default_graph()
        self.black = QPlayer(tile)
        self.white = secondPlayer
        self.mainQN = QNetwork(tf,self.lr)
        self.view = view


    def run(self):
        init = tf.global_variables_initializer()
        winB = winW = 0
        with tf.Session() as sess:
            sess.run(init)
            for i in range(self.num_episodes):
                #Reset enviorement and start new board
                s = board.Board()
                #rAll = 0
                actualTurnPlayer = self.black
                passCount = 0
                #The Q-Network
                while s.getRemainingPieces() > 0 and passCount < 2:
                    possible_actions = actualTurnPlayer.checkMoves(s);
                    if possible_actions:
                        passCount = 0
                        if actualTurnPlayer == self.white:
                            move = actualTurnPlayer.getMove(possible_actions)
                            s.updateBoard(actualTurnPlayer.getTile(),move)
                        else:
                            #Choose an action by greedily (with e chance of random action) from the Q-network
                            Q = sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[s.get1DBoard()]})
                            if np.random.rand(1) < self.e:
                                action = random.choice(possible_actions)
                            else:
                                action = self.get_best_possible_action(possible_actions,Q)
                            #Get new state and reward from environment
                            sPrime,r = self.get_next_state(actualTurnPlayer.getTile(),action,copy.deepcopy(s))
                            #Obtain the Q' values by feeding the new state through our network
                            QPrime = sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[sPrime.get1DBoard()]})
                            #Obtain maxQ' and set our target value for chosen action.
                            Q[0,action] = r + self.y*np.max(QPrime)
                            #Train our network using target and predicted Q values
                            _ = sess.run([self.mainQN.updateModel,self.mainQN.W],feed_dict={self.mainQN.inputLayer:[s.get1DBoard()],self.mainQN.nextQ:Q})
                            #rAll += r
                            s = sPrime
                    else:
                        passCount += 1
                        #self.view.printCannotMove()
                    #Next turn
                    actualTurnPlayer = self.white if actualTurnPlayer is self.black else self.black
                #End Game: Reduce chance of random action as we train the model.
                self.e -= self.eDrop
                #self.rList.append(rAll)
                #Print final Board and score
                print "("+str(i)+")"
                #self.view.printScore(s,s.getScore())
                if self.black.getScore(s) > self.white.getScore(s):
                    winB += 1
                elif self.black.getScore(s) < self.white.getScore(s):
                    winW += 1
        print "Black wins: " + str(winB) + " - White wins: " + str(winW)
        #self.view.printEndGame
        #print("Percent of succesful episodes: " + str(sum(self.rList)/self.num_episodes) + "%")

    def get_next_state(self,tile,action,sPrime):
        """
        Update board and return new board and reward
        @param int tile
        @param int action
        @param Board sPrime
        @return Board,int sPrime,reward
        """
        sPrime.updateBoard(tile,action)
        reward = -1
        if sPrime.getScore()[tile] > sPrime.getScore()[-tile]:
            reward = 1
        return sPrime,reward

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
