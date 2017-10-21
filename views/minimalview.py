class MinimalView:

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

    def isTrainning(self):
        """ Ask if the IA will train """
        print("Do you want to train the IA?")
        while True:
            num_episodes = raw_input("Type [0] not train, > 0 to train : ")
            try:
                if int(num_episodes) == 0:
                    return False, 1
                elif int(num_episodes) > 0:
                    return True, int(num_episodes)
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

    def loadModel(self):
        """ Ask if want to load DQN trained model """
        print("Do you want to load previous model?")
        while True:
            load_model = raw_input("Type [y] to load, otherwise [n]: ")
            if load_model == 'y':
                return True
            if load_model == 'n':
                return False
            print("Invalid input, try again")
        return

    def printBoard(self,board):
        pass

    def printScore(self,board,score):
        pass

    def printState(self,board):
        pass

    def printTurn(self,board,tile):
        pass

    def printInvalidMove(self):
        pass

    def printCannotMove(self):
        pass

    def printEndGame(self):
        pass
