import numpy

class Board(object):
    BLACK = 1
    WHITE = -1

    def __init__(self):
        self.board = numpy.zeros((8,8), int)
        self.board[3][3] = Board.WHITE
        self.board[4][4] = Board.WHITE
        self.board[3][4] = Board.BLACK
        self.board[4][3] = Board.BLACK

        self.remaining_pieces = 8*8-4
        self.score = {Board.BLACK: 2, Board.WHITE: 2}

    def getScore(self):
        """ Returns actual score """
        return self.score

    def getBoard(self):
        """ Returns actual state of board """
        return self.board

    def get1DBoard(self):
        """ Returns actual state of board in 1 Dimension"""
        return self.board.reshape((64))

    def get129Board(self,tile):
        """ Returns actual state of board in 1 Dimension of 128 positions,
        half for black pieces positions, other half for white positions """
        oneD = self.get1DBoard()
        shapedBoard = numpy.zeros(129,int)
        idx = 0
        for pos in oneD:
            if pos == 0:
                shapedBoard[idx] = 0
                shapedBoard[idx+64] = 0
            elif pos == self.BLACK:
                shapedBoard[idx] = 1
            else:
                shapedBoard[idx+64] = 1
            idx += 1

        shapedBoard[128] = (1+tile)/2
        return shapedBoard

    def isOnBoard(self,c,r):
        """ Returns true if valid position or false otherwise """
        return (c>=0) and (c<=7) and (r>=0) and (r<=7)

    def getRemainingPieces(self):
        """ Returns remaining pieces """
        return self.remaining_pieces

    def next(self,tile,action):
        """
        Update board and return new board and reward
        @param int tile
        @param int action
        @param Board s
        @return Board,int,bool sPrime,reward,d
        """
        self.updateBoard(tile,action)
        reward = -1
        d = 0
        if self.getScore()[tile] > self.getScore()[-tile]:
            reward = 1
        if self.getRemainingPieces() == 0:
            d = 1
        return self,reward,d


    def updateBoard(self,tile,move):
        """
        Updates board with new movement if is a valid move
        @param int tile
            1 for BLACK
            -1 for WHITE
        @param int move
            0-63 vector position
        """
        row = move // 8
        col = move % 8
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
