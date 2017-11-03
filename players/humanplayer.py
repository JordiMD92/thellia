from player import Player

class HumanPlayer(Player):

    def __init__(self,tile,view):
        Player.__init__(self,tile)
        self.view = view

    def getMove(self,board,possibleMoves,total_steps):
        """
        Get the player's move
        @param board board
        @param list(int) possibleMoves
        @param int total_steps
        @return int position
        """
        return self.view.askMove(possibleMoves)
