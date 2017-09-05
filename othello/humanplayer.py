from player import Player

class HumanPlayer(Player):

    def __init__(self,tile,view):
        Player.__init__(self,tile)
        self.view = view

    def getMove(self,posibleMoves):
        return self.view.askMove(posibleMoves)
