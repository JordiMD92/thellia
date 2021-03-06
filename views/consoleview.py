import os

class ConsoleView:

    def getGameMode(self,game):
        print("Welcome to Thellia")
        print("Choose a game mode:")
        print(str(game.GameMode['hvh'])+") Human vs Human")
        print(str(game.GameMode['hvr'])+") Human vs Random Computer")
        print(str(game.GameMode['rvr'])+") Random Computer vs Random Computer")
        print(str(game.GameMode['qvq'])+") DQN AI vs DQN AI")
        print(str(game.GameMode['qvh'])+") DQN AI vs Human")
        print(str(game.GameMode['qvr'])+") DQN AI vs Random Computer")
        while True:
            gameMode = int(input("Please choose: "))
            if gameMode >= 1 and gameMode <= len(game.GameMode):
                return gameMode
            else:
                print("Invalid option, try again")

    def getHumanTile(self):
        print("Pick a tile color, Black moves first")
        print("1) Black \n2) White")
        while True:
            tile = int(input("Pick 1 or 2: "))
            if tile == 1 or tile == 2:
                return tile
            else:
                print("Invalid option, try again")

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

    def getTrainEpisodes(self):
        """ Ask if the IA will train """
        print("Do you want to train the IA?")
        while True:
            num_episodes = raw_input("Type number iterations to train, [0] to not train: ")
            try:
                if int(num_episodes) >= 0:
                    return int(num_episodes)
                print("Invalid input, try again")
            except:
                print("Invalid input, try again")
        return

    def loadGames(self):
        """ Ask if want to load human games """
        print("Do you want to load games from DB?")
        while True:
            load_episodes = raw_input("Type [0] not load, > 0 to load, [all] to load all: ")
            if load_episodes == "all":
                return load_episodes
            try:
                if int(load_episodes) >= 0:
                    return int(load_episodes)
                print("Invalid input, try again")
            except:
                print("Invalid input, try again")
        return

    def loadModel(self,path):
        """ Ask if want to load DQN trained model """
        print("Do you want to load previous model?")
        models = os.walk(path).next()[1]
        i = 0
        for model in models:
            i+=1
            print "["+str(i)+"] "+model
        while True:
            load_model = raw_input("Type [0] not to load, otherwise > 1: ")
            try:
                if int(load_model) == 0:
                    return False
                elif int(load_model) > 0 and int(load_model) <= len(models):
                    return models[int(load_model)-1]
                print("Invalid input, try again")
            except:
                print("Invalid input, try again")
        return

    def printBoard(self,board):
        """ Print actual board state """
        print("   A   B   C   D   E   F   G   H  ")
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
            print "\n\nBlack turn 'O'"
        else:
            print "\n\nWhite turn 'X'"

    def printInvalidMove(self):
        """ Print invalid move """
        print "Invalid move! Try again"

    def printCannotMove(self):
        """ Print can't move """
        print "Can't move! :("

    def printEndGame(self):
        """ Print end game """
        print "Game ended, thanks for playing! :)"
