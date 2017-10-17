from player import Player

class HumanPlayer(Player):

    def __init__(self,tile,view):
        Player.__init__(self,tile)
        self.view = view

    def getMove(self,possibleMoves):
        """
        Get the player's move
        @param list(int) possibleMoves
        @return int position
        """
        return self.view.askMove(possibleMoves)
