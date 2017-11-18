from player import Player
import numpy as np
import random
from copy import deepcopy

class QPlayer(Player):

    def __init__(self,tile,QN,train,num_episodes):
        Player.__init__(self,tile=tile)
        self.QN = QN
        self.model = self.QN.getModel()
        self.train = train
        self.num_episodes = num_episodes
        self.e = 1
        if QN.isModelLoaded():
            self.e = 0.1
        if train == "play" or train == "load":
            self.e = -1
        self.y = 0.99

    def updateEpsilon(self):
        """ Update e greedy """
        if self.e > 0.01:
            self.e -= (0.9/self.num_episodes)

    def getMove(self,s,possibleMoves):
        """ Get the player's move
        @param board s
        @param list(int) possibleMoves
        @return int action
        """
        boardShape = s.getBoardShape(self.QN.getInputShape(),self.tile)
        Qout = self.model.predict(boardShape,batch_size=1)
        #Choose move e-greedyly, random or from network
        if np.random.rand(1) < self.e:
            action = random.choice(possibleMoves)
        else:
            action = self.get_best_possible_action(possibleMoves,Qout)

        if self.train != "play": #train == "train" or train == "load"
            #Get new state and reward from environment and update
            sPrime,r,done = s.next(self.tile,action)
            self.QN.addExperience(s,action,r,sPrime,done)
            #Train when mem if it's len is at least batch_size
            if self.QN.batch_size < len(self.QN.memBuffer):
                trainBatch = self.QN.sample()
                for s_batch,a_batch,r_batch,sP_batch,d_batch in trainBatch:
                    sBoardShape = s_batch.getBoardShape(self.QN.getInputShape(),self.tile)
                    sPBoardShape = sP_batch.getBoardShape(self.QN.getInputShape(),self.tile)
                    Qout = self.model.predict(sBoardShape,batch_size=1)
                    maxQ1 = np.max(self.model.predict(sPBoardShape,batch_size=1))
                    targetQ = deepcopy(Qout)
                    targetQ[0,a_batch] = r_batch if d_batch else r_batch + self.y*maxQ1
                    self.model.fit(Qout,targetQ,epochs=1,verbose=0)
                    if d_batch:
                        self.updateEpsilon()
        return action

    def get_best_possible_action(self,possible_moves,moves):
        """
        Get the best possible move from a list
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

    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "QP"
