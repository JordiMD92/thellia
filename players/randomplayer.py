from player import Player
import random

class RandomPlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile=tile)

    def getMove(self,game,board,possibleMoves,tile):
        """
        Get the player's move
        @param Board board
        @param list(int) possibleMoves
        @return int position
        """
        return random.choice(possibleMoves)

    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "RP"
