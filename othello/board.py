import numpy

class Board(object):
    BLACK = 1
    WHITE = -1

    def __init__(self):
        self.board = numpy.zeros((8,8), int)
        self.board[3][3] = Board.BLACK
        self.board[4][4] = Board.BLACK
        self.board[3][4] = Board.WHITE
        self.board[4][3] = Board.WHITE

        self.remaining_pieces = 8*8-4
        self.score = {Board.BLACK: 2, Board.WHITE: 2}

    def getScore(self):
        """ Returns actual score """
        return self.score

    def getBoard(self):
        """ Returns actual state of board """
        return self.board

    def isOnBoard(self,c,r):
        """ Returns true if valid position or false otherwise """
        return (c>=0) and (c<=7) and (r>=0) and (r<=7)

    def getRemainingPieces(self):
        """ Returns remaining pieces """
        return self.remaining_pieces

    def updateBoard(self,tile,col,row):
        """
        Updates board with new movement if is a valid move
        @param int tile
            1 for BLACK
            -1 for WHITE
        @param int row
            0-7 row position
        @param int col
            0-7 column position
        """
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
        @param int row
            0-7 row position
        @param int col
            0-7 column position
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
