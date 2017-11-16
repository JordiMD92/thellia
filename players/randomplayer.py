from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile)

    def getMove(self,board,possibleMoves):
        """
        Get the player's move
        @param Board board
        @param list(int) possibleMoves
        @return int position
        """
        return random.choice(possibleMoves)

    def updateEpsilon(self):
        pass
