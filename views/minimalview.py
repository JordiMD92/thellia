import os
class MinimalView:

    def getGameMode(self,gameMode):
        print("Choose a game mode:")
        print(str(gameMode['hvh'])+") Human vs Human")
        print(str(gameMode['hvr'])+") Human vs Random Computer")
        print(str(gameMode['rvr'])+") Random Computer vs Random Computer")
        print(str(gameMode['qvq'])+") DQN AI vs DQN AI")
        print(str(gameMode['qvh'])+") DQN AI vs Human")
        print(str(gameMode['qvr'])+") DQN AI vs Random Computer")
        while True:
            mode = int(input("Please choose: "))
            if mode >= 1 and mode <= len(gameMode):
                return mode
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

    def getNumEpisodes(self,db=False):
        """ Ask how much the IA will play """
        print("How many games do you want to run?")
        while True:
            if db:
                num_episodes = raw_input("Type number games to load, [0] to not load or \"all\" to load all db: ")
                if num_episodes == "all":
                    return num_episodes
            else:
                num_episodes = raw_input("Type number iterations to run, [0] to not play: ")
            try:
                if int(num_episodes) >= 0:
                    return int(num_episodes)
                print("Invalid input, try again")
            except:
                print("Invalid input, try again")
        return

    def getMode(self):
        """ Ask which mode want to run """
        print("What mode want to run?")
        while True:
            mode = raw_input("Type \"load\" to load DB, \"train\" to train AI, \"play\" to play: ")
            try:
                if mode == "load" or mode == "train" or mode == "play":
                    return mode
                print("Invalid input, try again")
            except:
                print("Invalid input, try again")
        return

    def loadModel(self,path):
        """ Ask if want to load DQN trained model """
        print("Do you want to load previous model?")
        folders = os.walk(path).next()[1]
        models = []
        i = 0
        for folder in folders:
            try:
                os.rmdir(path+"/"+folder)
            except:
                models.append(folder)
        for model in models:
            i+=1
            print "["+str(i)+"] "+model
        while True:
            load_model = raw_input("Type [0] not to load, otherwise > 1: ")
            try:
                if int(load_model) == 0:
                    return False
                elif int(load_model) > 0 and int(load_model) <= len(models):
                    return path+"/"+models[int(load_model)-1]
                print("Invalid input, try again")
            except:
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
