import os
class MinimalView:

    def printBoard(self,board):
        """ Print actual board state """
        print("   A   B   C   D   E   F   G   H  ")
        print(" - - - - - - - - - - - - - - - - -")
        for r in range(0,8,1):
            row = ""
            for c in range(0,8,1):
                value = "|   "
                if board[c][r] == -1: value = "| W "
                if board[c][r] == 1: value = "| B "
                row = row+value
            print(str(r+1)+row+"|")
            print(" - - - - - - - - - - - - - - - - -")


    def askMove(self,posibleMoves):
        """ Ask what move the player will do """
        print("Where will you move?")
        while True:
            pos = raw_input("Type Colum and Row 'CR' Ex:a1 for first column/row: ")
            if len(pos) == 2:
                c = ord(pos[0])-97
                r = int(pos[1])-1
                move = c+r*8
                if move in posibleMoves:
                    return move
                print("Invalid move, try again")
        return
