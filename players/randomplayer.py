from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile)

    def getMove(self,possibleMoves):
        """
        Get the player's move
        @param list(int) possibleMoves
        @return int position
        """
        return random.choice(possibleMoves)
