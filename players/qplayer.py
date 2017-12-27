from player import Player
import numpy as np
import random
import tensorflow as tf

class QPlayer(Player):

    def __init__(self,tile,QN,mode,num_episodes,train):
        Player.__init__(self,tile=tile)
        self.QN = QN
        self.model = self.QN.getModel()
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
        s = board.getBoardState()
        s = s.reshape((-1,board.getBoardSize())) #(1,Board.SIZE)
        Qout = self.model.predict(s)
        #Choose move e-greedyly, random or from network
        if np.random.rand(1) < self.e and self.mode == "train":
            action = random.choice(possibleMoves)
        else:
            action = self.get_best_possible_action(possibleMoves,Qout,board)
        self.conta += 1

        if self.mode != "play" and self.train: #mode == "train" or mode == "load"
            #Get new state and reward from environment and update
            sPrime,r,done = game.next(board,action,self.tile)
            self.QN.addExperience(s,action,r,sPrime,done)
            #Train when mem if it's len is at least batch_size
            if self.conta % self.updateFreq == 0 and self.conta >= self.QN.batch_size:                
                trainBatch = self.QN.sample()
                inputs = np.zeros((self.QN.batch_size,board.getBoardSize()))
                targets = np.zeros((self.QN.batch_size,board.getBoardSize()))
                for i in range(self.QN.batch_size):
                    s_batch,a_batch,r_batch,sP_batch,d_batch = trainBatch[i]
                    inputs[i] = s_batch
                    targets[i] = self.model.predict(inputs[i].reshape((-1,board.getBoardSize()))) #Qout
                    if d_batch:
                        targets[i,a_batch] = r_batch
                        self.updateEpsilon()
                    else:
                        maxQ1 = np.max(self.model.predict(sP_batch.reshape((-1,board.getBoardSize())))) #(1,Board.SIZE)
                        targets[i,a_batch] = r_batch + self.y*maxQ1
                loss = self.model.train_on_batch(inputs, targets)
                summary = tf.Summary(value=[tf.Summary.Value(tag="loss",simple_value=loss),])
                self.QN.tbWriter.add_summary(summary)
        return action

    def get_best_possible_action(self,possible_moves,moves,board):
        """
        Get the best possible move from a list
        @param list(int) possible_moves
        @param list(int) moves
        @return int move
        """
        #Sort network moves from high to low
        sorted_moves = [(val,i) for i,val in enumerate(moves[0])]
        sorted_moves.sort(key = lambda x: x[0], reverse = True)
        for move in sorted_moves:
            if move[1] in possible_moves:
                return move[1]
        return possible_moves[0] #not possible

    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "QP"
