from player import Player
import numpy as np
import random

class QPlayer(Player):

    def __init__(self,tile,QN,train,num_episodes):
        Player.__init__(self,tile)
        self.QN = QN
        self.model = self.QN.get_model()
        self.train = train
        self.num_episodes = num_episodes
        self.e = 1
        if not train or train == "load":
            self.e = -1
        if QN.isModelLoaded():
            self.e = 0.1
        self.y = 0.99
        self.conta = 0

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

        if self.train:
            #Get new state and reward from environment and update
            sPrime,r = s.next(self.tile,action)
            sPrimeBoardShape = sPrime.getBoardShape(self.QN.getInputShape(),self.tile)
            Q1 = self.model.predict(sPrimeBoardShape,batch_size=1)
            maxQ1 = np.max(Q1)
            targetQ = Qout
            targetQ[0,action] = r + self.y*maxQ1
            self.model.fit(Qout,targetQ,epochs=1,verbose=0)

            self.conta += 1
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
