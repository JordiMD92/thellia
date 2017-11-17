from __future__ import division
import os
import timeit
import time
import board
from players.randomplayer import RandomPlayer

class Game:

    def __init__(self, view, b, w):
        self.view = view
        self.b = b
        self.w = w
        self.board = board.Board()

    def reset(self):
        """ Reset environment """
        self.board = board.Board()

    def gameStart(self, dbGame=[]):
        """ Game engine to play Othello, switch between players and do moves
        @param list(int) dbGame
        """
        # Get black player, first to move
        if self.b.getTile() == self.board.BLACK:
            black = self.b
            white = self.w
        else:
            black = self.w
            white = self.b
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

    def train(self, num_episodes, dbGames=[]):
        """ Train othello game, run games for especified num_episodes
        @param int num_episodes
        @param list(list(int)) dbGames
        @return list(int,int) wins
        """
        start = timeit.default_timer()
        wins = []

        # Train #num_episodes
        for i in range(num_episodes):
            dbGame = []
            if dbGames:
                dbGame = dbGames[i]
            self.gameStart(dbGame)
            # Update e for QPlayer
            self.b.updateEpsilon()
            self.w.updateEpsilon()

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
        return wins

    def play(self,num_episodes):
        """ Play othello game, run games for especified num_episodes
        @param int num_episode
        @return list(int,int) wins
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
                print wins
            if i % 1000 == 0 and i > 0:
                print "("+str(i)+") Black wins: " + str(winB/i * 100) + "% - White wins: " + str(winW/i * 100) + "%"
                pause = timeit.default_timer()
                print "Temps: " + str(pause-start)

            if self.b.getScore(self.board) > self.w.getScore(self.board):
                winB += 1
            elif self.b.getScore(self.board) < self.w.getScore(self.board):
                winW += 1
        # Save wins and show time
        wins.append(((winB/num_episodes*100),(winW/num_episodes*100)))
        stop = timeit.default_timer()
        print "Temps Final: " + str(stop-start)
        print "Black wins: " + str(winB/num_episodes*100) + "% - White wins: " + str(winW/num_episodes*100) + "%"
        return wins

    def playRandomBatch(self):
        """ Play 100 Random games versus AI
        @return int,int winB,winW
        """
        print "-- Percentage batch 100 Random games --"
        tempB = self.b
        tempW = self.w
        self.w = RandomPlayer(-1)
        winB = winW = 0

        for i in range(100):
            self.gameStart()

            if self.b.getScore(self.board) > self.w.getScore(self.board):
                winB += 1
            elif self.b.getScore(self.board) < self.w.getScore(self.board):
                winW += 1
        print "Black wins: " + str(winB) + "% - White wins: " + str(winW) + "%"
        print "----------------------------------------"
        self.b = tempB
        self.w = tempW
        return winB,winW

    def loadGames(self, db_path, num_episodes):
        """ Load professional saved games
        @param String db_path
        @param int num_episodes
        @return list(int,int) wins
        """
        dbGames = []
        with open(db_path, 'r') as f:
            #Open file and read all
            lines = f.readlines()
            lines = [ line.strip() for line in lines ]
            if num_episodes == "all" or num_episodes > len(lines):
                num_episodes = len(lines)
            for idx in range(num_episodes):
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
                dbGames.append(newLine)
        if dbGames:
            wins = self.train(num_episodes,dbGames)
            return wins
        return
