import board

class Game():

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
        while self.board.getRemainingPieces > 0 or passCount == 2:
            #Print actual board, score and turn
            view.printState(self.board)
            view.printTurn(self.board,actualTurnPlayer.getTile())
            #Get move and update board if possible, otherwise pass
            move = view.askMove(actualTurnPlayer,board)
            if move:
                if self.board.updateBoard(actualTurnPlayer.getTile(),move[0],move[1]):
                    passCount = 0
                else:
                    view.printInvalidMove()
                    continue
            else:
                passCount += 1
            actualTurnPlayer = white if actualTurnPlayer is black else black
        #Print final Board and score
        view.printState(self.board)
