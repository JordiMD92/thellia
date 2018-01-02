from player import Player

class MaxTilePlayer(Player):

    def __init__(self,tile):
        Player.__init__(self,tile=tile)

    def getMove(self,game,board,possibleMoves,tile):
        """
        Get the player's move
        @param Board board
        @param list(int) possibleMoves
        @return int position
        """
        final_value = -99
        final_move = -1
        for move in possibleMoves:
            r = move // board.SIZE
            c = move % board.SIZE
            if final_value < board.FITBOARD[c][r]:
                final_value = board.FITBOARD[c][r]
                final_move = move
        return final_move


    @classmethod
    def getType(self):
        """ Returns players type
        @return string type
        """
        return "MP"
