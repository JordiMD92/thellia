from player import Player

class HumanPlayer(Player):

    def __init__(self,tile,view):
        Player.__init__(self,tile)
        self.view = view

    def getMove(self,board):
        r = c = -1
        #Check posible moves
        posibleMoves = self.checkMoves(board)
        if posibleMoves:
            c,r = self.view.askMove(posibleMoves)
        return c,r
