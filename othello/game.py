import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import board
from players.qplayerUpdated import QPlayer

class Game:
    GameMode = {'hvh': 1,'hvr': 2,'rvr': 3,'qvq': 4,'qvh': 5,'qvr': 6}

    def __init__(self, view):
        self.view = view
        self.players = []
        self.board = board.Board()
        self.total_steps = 0

    def addPlayers(self, p1, p2):
        """ Add players to the game
        @param Player p1
        @param Player p2
        """
        self.players.append(p1)
        self.players.append(p2)

    def getPlayers(self):
        """ Return players
        @return Player,Player
        """
        return self.players[0],self.players[1]

    def getScore(self):
        """ Get game score
        @return [int,int] score
        """
        return self.board.getScore()

    def reset(self):
        """ Reset environment """
        self.board = board.Board()

    def setView(self, view):
        """ Set new view to Game
        @param View view
        """
        self.view = view

    def run(self, num_episodes=1, gamesDB=[]):
        """ Run othello game, run games for especified num_episodes
        @param int num_episode
        @param list(list(int)) gamesDB
        """
        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            # Set session for QPlayer
            self.players[0].setSession(sess)
            self.players[1].setSession(sess)

            for i in range(num_episodes):
                actualGame = []
                if gamesDB:
                    actualGame = gamesDB[i]
                else:
                    print "Espisode: "+str(i+1)
                self.reset()
                self.gameStart(actualGame)
                # Update buffers and e for QPlayer
                if isinstance(self.players[0],QPlayer):
                    self.players[0].endGame(num_episodes)
                if isinstance(self.players[1],QPlayer):
                    self.players[1].endGame(num_episodes)

    def gameStart(self, actualGame=[]):
        """ Game engine to run Othello, switch between players and do moves
        @param list(int) actualGame
        """
        # Get black player, first to move
        if self.players[0].getTile() == self.board.BLACK:
            black = self.players[0]
            white = self.players[1]
        else:
            black = self.players[1]
            white = self.players[0]
        actualTurnPlayer = black
        passCount = 0
        while self.board.getRemainingPieces() > 0 and passCount < 2:
            # Play if there are pieces and can do a move
            self.view.printState(self.board)
            self.view.printTurn(self.board, actualTurnPlayer.getTile())
            possibleMoves = actualTurnPlayer.checkMoves(self.board)
            if possibleMoves:
                # If there are move, play
                passCount = 0
                if actualGame:
                    try:
                        # If it is loading from DB, get next move
                        possibleMoves = actualGame[60 - self.board.getRemainingPieces]
                    except:
                        break
                #Get player move and update board
                move = actualTurnPlayer.getMove(self.board, possibleMoves, self.total_steps)
                self.board.updateBoard(actualTurnPlayer.getTile(), move)
                self.total_steps += 1
            else:
                #If there aren't moves, switch player
                passCount += 1
                self.view.printCannotMove()
            actualTurnPlayer = white if actualTurnPlayer is black else black

        self.view.printState(self.board)
        self.view.printEndGame()

    def loadGames(self, path,load_episodes):
        """ Load professional saved games
        @param String path
        @param int load_episodes
        @return list(list(int)) games(moves)
        """
        with open(path, 'r') as f:
            #Open file and read all
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
            newLines = []
            if load_episodes == "all" or load_episodes > len(lines):
                load_episodes = len(lines)
            for idx in range(load_episodes):
                # Put on memory only the number of games to play and return
                newLine = []
                i = 1
                for char in lines[idx]:
                    if i % 2 == 0 and i > 0:
                        move = ord(preChar) - 97 + (int(char) - 1) * 8
                        newLine.append(move)
                    else:
                        preChar = char
                    i += 1
                newLines.append(newLine)
        return newLines,load_episodes
