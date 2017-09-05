from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile)

    def getMove(self,posibleMoves):
        return random.choice(posibleMoves)
