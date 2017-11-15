from __future__ import division
import os
import timeit
import time
import board
from players.randomplayer import RandomPlayer
from othello.process_results import ProcessResults

class Game:

    def __init__(self, view, p1, p2, path, sess):
        self.view = view
        self.p1 = p1
        self.p2 = p2
        self.path = path
        self.sess = sess
        self.board = board.Board()
        self.pr = ProcessResults()

        self.gameModel = path+"/"+time.strftime("%Y-%m-%d_%H:%M:%S")
        #Make a path for our model to be saved in.
        if not os.path.exists(self.gameModel):
            os.makedirs(self.gameModel)

    def getPlayers(self):
        """ Return players
        @return Player,Player
        """
        return self.p1,self.p2

    def getScore(self):
        """ Get game score
        @return [int,int] score
        """
        return self.board.getScore()

    def reset(self):
        """ Reset environment """
        self.board = board.Board()

    def gameStart(self, dbGame=[]):
        """ Game engine to play Othello, switch between players and do moves
        @param list(int) dbGame
        """
        # Get black player, first to move
        if self.p1.getTile() == self.board.BLACK:
            black = self.p1
            white = self.p2
        else:
            black = self.p2
            white = self.p1
        actualTurnPlayer = black
        # Reset board
        self.reset()
        passCount = 0
        while self.board.getRemainingPieces() > 0 and passCount < 2:
            # Play if there are pieces and can do a move
            possibleMoves = actualTurnPlayer.checkMoves(self.board)
            if possibleMoves:
                # If there is a move, play
                passCount = 0
                if dbGame:
                    try:
                        # If it is loading from DB, get next move
                        possibleMoves = [dbGame[60 - self.board.getRemainingPieces()]]
                    except:
                        break
                #Get player move and update board
                move = actualTurnPlayer.getMove(self.board, possibleMoves)
                self.board.updateBoard(actualTurnPlayer.getTile(), move)
            else:
                #If there aren't moves, pass
                passCount += 1
            actualTurnPlayer = white if actualTurnPlayer is black else black

    def train(self, num_episodes=100, gamesDB=[]):
        """ Train othello game, run games for especified num_episodes
        @param int num_episodes
        @param list(list(int)) gamesDB
        @return String gameModel
        """
        start = timeit.default_timer()
        wins = []

        # Train #num_episodes
        for i in range(num_episodes):
            dbGame = []
            if gamesDB:
                dbGame = gamesDB[i]
            self.gameStart(dbGame)
            # Update e for QPlayer
            self.p1.updateEpsilon()
            self.p2.updateEpsilon()

            if i % 100 == 0 and i > 0:
                print "{"+str(i)+" - "+str(num_episodes)+"}"
            # Save wins and show time
            if i % 1000 == 0 and i > 0:
                pause = timeit.default_timer()
                print "Temps: " + str(pause-start)
                winB,winW = self.playRandomBatch()
                wins.append(((winB),(winW)))

        # Save wins and show time
        winB,winW = self.playRandomBatch()
        wins.append(((winB),(winW)))
        stop = timeit.default_timer()
        print "Temps Final: " + str(stop-start)
        self.pr.saveResults(wins,self.gameModel)
        return self.gameModel

    def play(self,num_episodes=100):
        """ Play othello game, run games for especified num_episodes
        @param int num_episode
        @return String gameModel
        """
        start = timeit.default_timer()
        winB = winW = 0
        wins = []

        # Play #num_episodes
        for i in range(num_episodes):
            self.gameStart()

            # Save wins and show time
            if i % 100 == 0 and i > 0:
                wins.append(((winB/i*100),(winW/i*100)))
                print "{"+str(i)+" - "+str(num_episodes)+"}"
                print wins
            if i % 1000 == 0 and i > 0:
                print "("+str(i)+") Black wins: " + str(winB/i * 100) + "% - White wins: " + str(winW/i * 100) + "%"
                pause = timeit.default_timer()
                print "Temps: " + str(pause-start)

            if self.getScore()[self.board.BLACK] > self.getScore()[self.board.WHITE]:
                winB += 1
            elif self.getScore()[self.board.BLACK] < self.getScore()[self.board.WHITE]:
                winW += 1
        # Save wins and show time
        wins.append(((winB/num_episodes*100),(winW/num_episodes*100)))
        stop = timeit.default_timer()
        print "Temps Final: " + str(stop-start)
        print "Black wins: " + str(winB/num_episodes*100) + "% - White wins: " + str(winW/num_episodes*100) + "%"
        print "----------------------------------------"
        self.pr.saveResults(wins,self.gameModel)
        return self.gameModel

    def playRandomBatch(self):
        """ Play 100 Random games versus AI """
        print "-- Percentage batch 100 Random games --"
        tempP1 = self.p1
        tempP2 = self.p2
        self.p2 = RandomPlayer(-1)
        winB = winW = 0

        for i in range(100):
            self.gameStart()

            if self.getScore()[self.board.BLACK] > self.getScore()[self.board.WHITE]:
                winB += 1
            elif self.getScore()[self.board.BLACK] < self.getScore()[self.board.WHITE]:
                winW += 1
        print "Black wins: " + str(winB) + "% - White wins: " + str(winW) + "%"
        print "----------------------------------------"
        self.p1 = tempP1
        self.p2 = tempP2
        return winB,winW

    def loadGames(self, path, load_episodes):
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
            self.train(load_episodes,newLines)
            return self.gameModel
