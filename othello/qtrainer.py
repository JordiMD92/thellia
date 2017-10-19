from __future__ import division
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np
from collections import deque
import random
import copy
import tensorflow as tf
import board
from qnetwork import QNetwork
from experience_replay import ExperienceBuffer
from players.qplayer import QPlayer
from experience_replay import updateTarget
from experience_replay import updateTargetGraph

class QTrainer():

    def __init__(self,tile,secondPlayer,gamesDB,view):
        # Set learning parameters
        self.num_episodes = 10000
        self.lr = 0.01
        self.y = 0.99
        self.e = 1
        self.eDrop = 0.9 / self.num_episodes
        self.tau = 0.001 #Amount to update target network at each step.
        self.batch_size = 32 #Size of training batch
        self.pre_train_steps = 25000 #Number of steps used before training updates begin.
        self.total_steps = 0
        self.path = "./dqn" #The path to save our model to.

        # Set players, view and networks
        tf.reset_default_graph()
        self.black = QPlayer(tile,False)
        self.white = secondPlayer
        self.mainQN = QNetwork(tf,self.lr)
        self.targetQN = QNetwork(tf,self.lr)
        self.view = view

        self.load_DB = False
        self.games_DB = gamesDB
        if self.games_DB:
            #self.num_episodes = len(self.games_DB)
            self.load_DB = True

    def run(self,load_model):
        winB = winW = 0
        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        trainables = tf.trainable_variables()
        targetOps = updateTargetGraph(trainables,self.tau)
        myBuffer = ExperienceBuffer()

        #Make a path for our model to be saved in.
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with tf.Session() as sess:
            sess.run(init)

            if load_model == True:
                print "Loading Model..."
                ckpt = tf.train.get_checkpoint_state(self.path)
                saver.restore(sess,ckpt.model_checkpoint_path)

            print "Training Model... : " + str(self.num_episodes) +" episodes"
            for i in range(self.num_episodes):
                print "("+str(i+1)+")"
                gameBuffer = ExperienceBuffer()
                #Reset enviorement and start new board
                s = board.Board()
                actualTurnPlayer = self.black
                passCount = 0
                if self.load_DB:
                    actualGame = self.games_DB[i]

                #The Q-Network
                while s.getRemainingPieces() > 0 and passCount < 2:
                    possible_actions = actualTurnPlayer.checkMoves(s);
                    if possible_actions:
                        passCount = 0
                        if actualTurnPlayer == self.white:
                            if self.load_DB:
                                try:
                                    action = actualGame[60-s.getRemainingPieces()]
                                except:
                                    break
                            else:
                                action = actualTurnPlayer.getMove(s,possible_actions)
                            s.updateBoard(actualTurnPlayer.getTile(),action)
                        else:
                            if self.load_DB:
                                try:
                                    action = actualGame[60-s.getRemainingPieces()]
                                except:
                                    break
                            else:
                                #Choose an action by greedily (with e chance of random action) from the Q-network
                                if np.random.rand(1) < self.e or self.total_steps < self.pre_train_steps:
                                    action = random.choice(possible_actions)
                                else:
                                    Q = sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[s.get1DBoard()]})
                                    action = self.get_best_possible_action(possible_actions,Q)
                            #Get new state and reward from environment
                            sPrime,r,d = self.get_next_state(actualTurnPlayer.getTile(),action,copy.deepcopy(s))

                            gameBuffer.add(np.reshape(np.array([s.get1DBoard(),action,r,sPrime.get1DBoard(),d]),[1,5]))

                            if self.total_steps > self.pre_train_steps and self.total_steps % 5 == 0:
                                #We use Double-DQN training algorithm
                                trainBatch = myBuffer.sample(self.batch_size)
                                Q1 = sess.run(self.mainQN.predict,feed_dict={self.mainQN.inputLayer:np.vstack(trainBatch[:,3])})
                                Q2 = sess.run(self.targetQN.Qout,feed_dict={self.targetQN.inputLayer:np.vstack(trainBatch[:,3])})
                                end_multiplier = -(trainBatch[:,4] - 1)
                                doubleQ = Q2[range(self.batch_size),Q1]
                                targetQ = trainBatch[:,2] + (self.y*doubleQ * end_multiplier)
                                _ = sess.run(self.mainQN.updateModel,feed_dict={self.mainQN.inputLayer:np.vstack(trainBatch[:,0]),self.mainQN.nextQ:targetQ,self.mainQN.actions:trainBatch[:,1]})
                                updateTarget(targetOps,sess)

                            s = sPrime
                            self.total_steps += 1
                    else:
                        passCount += 1
                    #Next turn
                    actualTurnPlayer = self.white if actualTurnPlayer is self.black else self.black
                #End Game: Reduce chance of random action as we train the model.
                self.e -= self.eDrop
                myBuffer.add(gameBuffer.buffer)
                #Periodically save the model.
                if i % 1000 == 0 and i > 0:
                    saver.save(sess,self.path+'/model-'+str(i)+'.ckpt')
                    print("Saved Model")
                    print "Black wins: " + str(winB/i * 100) + "% - White wins: " + str(winW/i * 100) + "%"
                #Update game wins
                if self.black.getScore(s) > self.white.getScore(s):
                    winB += 1
                elif self.black.getScore(s) < self.white.getScore(s):
                    winW += 1

            saver.save(sess,self.path+'/model-'+str(i)+'.ckpt')
        print "Black wins: " + str(winB/self.num_episodes*100) + "% - White wins: " + str(winW/self.num_episodes*100) + "%"
        self.view.printEndGame

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
        d = 0
        if sPrime.getScore()[tile] > sPrime.getScore()[-tile]:
            reward = 1
        if sPrime.getRemainingPieces() == 0:
            d = 1
        return sPrime,reward,d

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
