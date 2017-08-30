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

    def updateBoard(self,tile,row,col):
        """
        Updates board with new movement if is a valid move
        @param int tile
            1 for BLACK
            -1 for WHITE
        @param int row
            0-7 row position
        @param int col
            0-7 column position
        @return bool
            true if valid - update board
            false if invalid move - doesn't update board
        """
        return False

    def isValidMove(self,tile,row,col):
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
        return flipTiles
