from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile)

    def getMove(self,board):
        r = c = -1
        #Check posible moves
        posibleMoves = self.checkMoves(board)
        if posibleMoves:
            c,r = random.choice(posibleMoves)
        return c,r
