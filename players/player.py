class Player:

    def __init__(self,tile):
        self.tile = tile

    def getScore(self,board):
        """ Returns actual player score
        @param Board board
        """
        return board.getScore()[self.tile]

    def getTile(self):
        """ Get players tile """
        return self.tile

    def checkMoves(self,board):
        """
        Check if the player can make a move
        @param Board board
        @return list(c+r*8)
            list of posible moves in 1 dimension format
        """
        posibleMoves = []

        for c in xrange(0,8):
            for r in xrange(0,8):
                if board.isValidMove(self.tile,c,r):
                    posibleMoves.append(c+r*8)

        return posibleMoves
