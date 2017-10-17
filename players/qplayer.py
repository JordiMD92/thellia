from player import Player

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import numpy as np
import tensorflow as tf

class QPlayer(Player):

    def __init__(self,tile,):
        Player.__init__(self,tile)
        #TODO update all the class
        #tf.reset_default_graph
        #createNetwork()
        #init = tf.global_variables_initializer()

    def createNetwork():
        #These lines establish the feed-forward part of the network used to choose actions
        inputLayer = tf.placeholder(shape=[1,64],dtype=tf.float32)
        W = tf.Variable(tf.random_uniform([64,64],0,0.01))
        Qout = tf.matmul(inputLayer,W)

    def getMove(self,board):
        r = c = -1

        posibleMoves = checkMoves(self.board)
        if posibleMoves:
            #Choose an action by greedily (with e chance of random action) from the Q-network
            actions = sess.run([Qout],feed_dict={inputLayer:[board.get1DBoard()]})
            pos = get_best_possible_action(possible_actions,actions)
        return pos[0],pos[1]

    """ Get the best move in possible player moves """
    def get_best_possible_action(possible_moves,moves):
        sorted_moves = [(val,i) for i,val in enumerate(moves)]
        sorted_moves.sort(key = lambda x: x[0], reverse = True)
        for move in sorted_moves:
            pos[0],pos[1] = move[0] // 8, move[0] % 8
            if pos in possible_moves:
                break
