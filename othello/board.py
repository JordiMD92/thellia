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
        self.passCount = 0
        self.score = {Board.BLACK: 2, Board.WHITE: 2}

    def getScore(self):
        """ Returns actual score """
        return self.score

    def getBoard(self):
        """ Returns actual state of board """
        return self.board

    def getBoardShape(self,num_positions,tile):
        """ Returns actual state of board in 1 Dimension of #input positions
        @param int num_positions
        @param int tile
        @return list(int) shapedBoard
        """
        oneD = self.board.reshape((-1,64))
        if num_positions == 64:
            # vector of 64 positions
            return oneD
        if num_positions == 129:
            # Half for black pieces positions, other half for white positions, last position = tile
            shapedBoard = numpy.zeros(129,int)
            idx = 0
            for pos in oneD[0]:
                if pos == 0:
                    shapedBoard[idx] = 0
                    shapedBoard[idx+64] = 0
                elif pos == self.BLACK:
                    shapedBoard[idx] = 1
                else:
                    shapedBoard[idx+64] = 1
                idx += 1

            shapedBoard[128] = (1+tile)/2
            return shapedBoard.reshape((-1,129))

    def isOnBoard(self,c,r):
        """ Returns true if valid position or false otherwise """
        return (c>=0) and (c<=7) and (r>=0) and (r<=7)

    def isEndGame(self):
        if self.remaining_pieces == 0 or self.passCount == 2:
            return True
        return False

    def next(self,tile,action):
        """
        Update board and return new board and reward
        @param int tile
        @param int action
        @return Board,int,bool sPrime,reward,done
        """
        self.updateBoard(tile,action)
        reward = 0
        if self.remaining_pieces == 0:
            reward = -1
            if self.getScore()[tile] > self.getScore()[-tile]:
                reward = 1
        return self,reward, self.isEndGame()

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
