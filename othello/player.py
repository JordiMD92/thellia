class Player(object):

    def __init__(self,tile):
        self.tile = tile

    def getScore(self,board):
        """ Returns actual player score """
        return board.getScore()[self.tile]

    def getTile(self):
        """ Get players tile """
        return self.tile

    def checkMoves(self,board):
        """ Check if the player can make a move """
        """ TODO
        for c in xrange(0,8):
            for r in xrange(0,8):
                r+=c
        """
        return True
