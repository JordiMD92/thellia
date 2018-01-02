import numpy as np
from copy import deepcopy

class Board(object):
    BLACK = 1
    WHITE = -1

    FITBOARD = [[99,-8,8,6,6,8,-8,99],
                [-8,-24,-4,-3,-3,-4,-24,-8],
                [8,-4,7,4,4,7,-4,8],
                [6,-3,4,0,0,4,-3,6],
                [6,-3,4,0,0,4,-3,6],
                [8,-4,7,4,4,7,-4,8],
                [-8,-24,-4,-3,-3,-4,-24,-8],
                [99,-8,8,6,6,8,-8,99]]

    SIZE = 8

    def __init__(self):
        self.board = np.zeros((Board.SIZE,Board.SIZE), int)
        self.board[3][3] = Board.WHITE
        self.board[4][4] = Board.WHITE
        self.board[3][4] = Board.BLACK
        self.board[4][3] = Board.BLACK

        self.remaining_pieces = Board.SIZE*Board.SIZE-4
        self.passCount = 0
        self.score = {Board.BLACK: 2, Board.WHITE: 2}

    def getScore(self):
        """ Returns actual score """
        return self.score

    def getBoard(self):
        """ Returns actual state of board """
        return self.board

    def getBoardState(self,tile):
        """ Returns actual state of board in 1 Dimension
        @return list(int) shapedBoard
        """
        output = 129
        oneD = self.board.reshape((pow(Board.SIZE,2)))
        if output == 64:
            return oneD
        return self.get129DBoard(oneD,tile)

    def get129DBoard(self,oneD,tile):
        """ Returns actual state of board in 1 Dimension of 129 positions,
        half for black pieces positions, other half for white positions + tile"""
        shapedBoard = np.zeros(129,int)
        idx = 0
        for pos in oneD:
            if pos == self.BLACK:
                shapedBoard[idx] = 1
            elif pos == self.WHITE:
                shapedBoard[idx+64] = 1
            idx += 1

        shapedBoard[128] = (1+tile)/2
        return shapedBoard

    def getBoardSize(self):
        """ Returns size of the board
        @return int boardSize
        """
        return pow(Board.SIZE,2)

    def isOnBoard(self,c,r):
        """ Returns true if valid position or false otherwise """
        return (c>=0) and (c<=Board.SIZE-1) and (r>=0) and (r<=Board.SIZE-1)

    def getWinner(self):
        if self.score[1] > self.score[-1]:
            return 1,0
        if self.score[1] < self.score[-1]:
            return 0,1
        return 0,0

    def isEndGame(self):
        if self.remaining_pieces == 0 or self.passCount == 2:
            return True
        return False

    def next(self,action,tile):
        """
        Update board and return new board and reward
        @param int tile
        @param int action
        @return Board[],int,bool sPrime,reward,done
        """
        sP = deepcopy(self)
        sP.updateBoard(tile,action)
        reward = 0
        if sP.isEndGame():
            reward = -1
            if sP.getScore()[tile] > sP.getScore()[-tile]:
                reward = 1
        return sP, reward, sP.isEndGame()

    def updateBoard(self,tile,move):
        """
        Updates board with new movement if is a valid move
        @param int tile
            1 for BLACK
            -1 for WHITE
        @param int move
            0-63 vector position
        @return bool can_move
        """
        row = move // Board.SIZE
        col = move % Board.SIZE
        moves = self.isValidMove(tile,col,row)
        if moves:
            self.board[col][row] = tile
            for position in moves:
                self.board[position[0]][position[1]] = tile
            self.score[tile] += len(moves) + 1
            self.score[-tile] -= len(moves)
            self.remaining_pieces -= 1
            return True
        else:
            return False

    def isValidMove(self,tile,col,row):
        """
        Checks if it is a valid move
        @param int tile
            1 for BLACK
            -1 for WHITE
        @param int col
            0-7 column position
        @param int row
            0-7 row position
        @return int[][]
            void if invalid move
            list of tiles to flip if valid move
        """
        flipTiles = []
        if self.board[col][row] != 0:
            return flipTiles

        for dirCol in ((-1),(0),(1)):
            for dirRow in ((-1),(0),(1)):
                if dirCol == dirRow and dirCol == 0:
                    continue
                c = dirCol + col
                r = dirRow + row
                while self.isOnBoard(c,r) and self.board[c][r] != 0:
                    if self.board[c][r] == tile:
                        while True:
                            c -= dirCol
                            r -= dirRow
                            if c == col and r == row:
                                break
                            flipTiles.append([c,r])
                    if self.board[c][r] + tile == 0:
                        c += dirCol
                        r += dirRow
        return flipTiles

    def get_fit_value(self,move):
        row = move // Board.SIZE
        col = move % Board.SIZE
        return Board.FITBOARD[row][col]
