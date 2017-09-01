class ConsoleView:
    def initMsg(self):
        print("Welcome to Thellia")
        print("Pick a tile color, Black moves first")
        print("1) Black \n2) White")
        while True:
            tile = int(input("Pick 1 or 2: "))
            if tile == 1 or tile == 2:
                return tile
            else:
                print("Invalid option, try again")

    def askMove(self,player,board):
        """ Ask what move the player will do """
        print("Where will you move?")
        if player.checkMoves(board):
            while True:
                move = raw_input("Type Colum and Row 'CR' Ex:a1 for first column/row: ")
                if len(move) == 2:
                    c = ord(move[0])-97
                    r = int(move[1])-1
                    if int(c) in xrange(0,8) and int(r) in xrange(0,8):
                        return c,r
                    else:
                        print("Invalid move, try again")
        return

    def printBoard(self,board):
        """ Print actual board state """
        print("\n\n   A   B   C   D   E   F   G   H  ")
        print(" - - - - - - - - - - - - - - - - -")
        for r in range(0,8,1):
            row = ""
            for c in range(0,8,1):
                value = "|   "
                if board[c][r] == -1: value = "| X "
                if board[c][r] == 1: value = "| O "
                row = row+value
            print(str(r+1)+row+"|")
            print(" - - - - - - - - - - - - - - - - -")

    def printScore(self,board,score):
        """ Print actual score """
        print("White score = "+str(score[board.WHITE]))
        print("Black score = "+str(score[board.BLACK]))

    def printState(self,board):
        """ Print board and score """
        self.printBoard(board.getBoard())
        self.printScore(board,board.getScore())

    def printTurn(self,board,tile):
        """ Print which turn is """
        if tile == board.BLACK:
            print "Black turn 'O'"
        else:
            print "White turn 'X'"

    def printInvalidMove(self):
        """ Print invalid move """
        print "Invalid move! Try again"
