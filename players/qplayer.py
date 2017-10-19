from player import Player

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from othello.qnetwork import QNetwork

class QPlayer(Player):

    def __init__(self,tile,load_model):
        Player.__init__(self,tile)
        path = "./dqn" #The path to save our model to.

        tf.reset_default_graph()
        self.mainQN = QNetwork(tf)

        init = tf.global_variables_initializer()
        saver = tf.train.Saver()
        self.sess = tf.InteractiveSession()
        self.sess.run(init)
        if load_model == True:
            print "Loading Model..."
            ckpt = tf.train.get_checkpoint_state(path)
            saver.restore(self.sess,ckpt.model_checkpoint_path)


    def getMove(self,board,possibleMoves):
        Q = self.sess.run(self.mainQN.Qout,feed_dict={self.mainQN.inputLayer:[board.get1DBoard()]})
        return self.get_best_possible_action(possibleMoves,Q)

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
