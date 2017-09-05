class Player:

    def __init__(self,tile):
        self.tile = tile

    def getScore(self,board):
        """ Returns actual player score """
        return board.getScore()[self.tile]

    def getTile(self):
        """ Get players tile """
        return self.tile

    def checkMoves(self,board):
        """
        Check if the player can make a move
        @param int[][] board
        @return list(c,r)
            list of posible moves in column/row format
        """
        posibleMoves = []

        for c in xrange(0,8):
            for r in xrange(0,8):
                if board.isValidMove(self.tile,c,r):
                    posibleMoves.append((c,r))

        return posibleMoves
