import board

class Game():
    GameMode = {'hvh': 1, 'hvr': 2, 'rvr': 3}

    def __init__(self):
        self.players = []
        self.board = board.Board()

    def addPlayer(self,player):
        """ Add a player to the game """
        self.players.append(player)

    def getScore(self):
        """ Get game score """
        return self.board.getScore()

    def run(self,view):
        """ Game engine to run Othello """
        if self.players[0].getTile() == self.board.BLACK:
            black = self.players[0]
            white = self.players[1]
        else:
            black = self.players[1]
            white = self.players[0]
        actualTurnPlayer = black
        passCount = 0
        while self.board.getRemainingPieces() > 0 and passCount < 2:
            #Print actual board, score and turn
            view.printState(self.board)
            view.printTurn(self.board,actualTurnPlayer.getTile())
            #Check posible moves, update board if possible otherwise pass
            posibleMoves = actualTurnPlayer.checkMoves(self.board)
            if posibleMoves:
                passCount = 0
                c,r = actualTurnPlayer.getMove(posibleMoves)
                self.board.updateBoard(actualTurnPlayer.getTile(),c,r)
            else:
                view.printCannotMove()
                passCount += 1
            actualTurnPlayer = white if actualTurnPlayer is black else black
        print "FINAL"
        #Print final Board and score
        view.printState(self.board)
