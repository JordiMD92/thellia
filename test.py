#!/usr/bin/env python
from othello.board import Board
from collections import defaultdict


class ConsoleView:
    def printBoard(self,board):
        print("   A   B   C   D   E   F   E   F  ")
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

    def printScore(self,score):
        print("White score = "+str(score[b.WHITE]))
        print("Black score = "+str(score[b.BLACK]))


b = Board();
cv = ConsoleView()

cv.printScore(b.getScore())
cv.printBoard(b.getBoard())

print "\n"
b.updateBoard(b.BLACK,1,4)
cv.printScore(b.getScore())
cv.printBoard(b.getBoard())
