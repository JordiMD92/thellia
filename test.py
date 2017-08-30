#!/usr/bin/env python
from othello.board import Board
from collections import defaultdict

b = Board();

print("White score = "+str(b.getScore()[b.WHITE]))
print("Black score = "+str(b.getScore()[b.BLACK]))

moves = str(b.isValidMove(b.BLACK,4,2))
print("is valid move? " + moves)
