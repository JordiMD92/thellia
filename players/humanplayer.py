from player import Player

class HumanPlayer(Player):

    def __init__(self,tile,view):
        Player.__init__(self,tile=tile)
        self.view = view

    def getMove(self,board,possibleMoves):
        """
        Get the player's move
        @param board board
        @param list(int) possibleMoves
        @param in num_game
        @return int position
        """
        self.view.printBoard(board.getBoard())
        return self.view.askMove(possibleMoves)

    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "HP"
