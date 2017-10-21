class Player:

    def __init__(self,tile,train=False):
        self.tile = tile
        self.sess = None
        self.train = train

    def setSession(self,sess):
        """ Update player tf session
        @param tfSession sess
        """
        self.sess = sess

    def setTrain(self,train):
        """ Update if player trains
        @param bool train
        """
        self.train = train

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

    def checkMoves(self,board):
        """
        Check if the player can make a move
        @param Board board
        @return list(c+r*8)
            list of posible moves in 1 dimension format
        """
        possibleMoves = []

        for c in xrange(0,8):
            for r in xrange(0,8):
                if board.isValidMove(self.tile,c,r):
                    possibleMoves.append(c+r*8)

        return possibleMoves
