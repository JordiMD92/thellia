from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile)

    def getMove(self,board,possibleMoves,total_steps):
        """
        Get the player's move
        @param list(int) possibleMoves
        @param int total_steps
        @return int position
        """
        return random.choice(possibleMoves)
