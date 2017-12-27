class Player:
    def __init__(self,tile):
        self.tile = tile

    def getScore(self,board):
        """ Returns actual player score
        @param Board board
        @return int score
        """
        return board.getScore()[self.tile]

    def getTile(self):
        """ Get players tile
        @return int tile
        """
        return self.tile

    def checkMoves(self,board,dbGame,idx):
        """
        Check if the player can make a move
        @param Board board
        @return list(c+r*board.SIZE)
            list of posible moves in 1 dimension format
        """
        possibleMoves = []
		#If dbGame, check same tile turn
        if idx < len(dbGame) and dbGame[idx][0] == self.tile:
			possibleMoves = [dbGame[idx][1]]
        else:
            for c in xrange(0,board.SIZE):
                for r in xrange(0,board.SIZE):
                    if board.isValidMove(self.tile,c,r):
                        possibleMoves.append(c+r*board.SIZE)

        return possibleMoves

    def setSession(self,sess,targetOps):
        self.sess = sess
        self.targetOps = targetOps
