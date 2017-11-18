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

    def gameStart(self, num_game, dbGame=[]):
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
        idx = 0
        while not self.board.endGame():
            if dbGame and idx < len(dbGame):
                #If dbGame, check same tile turn
                if dbGame[idx][0] == actualTurnPlayer.getTile():
                    passCount = 0
                    possibleMoves = [dbGame[idx][1]]
                    idx += 1
                else:
                    passCount += 1
                    possibleMoves = []
            else:
                #If not dbGame, get all possible moves
                possibleMoves = actualTurnPlayer.checkMoves(self.board)
            if possibleMoves:
                # If there is a move, get player move and update board
                passCount = 0
                move = actualTurnPlayer.getMove(self.board, possibleMoves, num_game)
                self.board.updateBoard(actualTurnPlayer.getTile(), move)
            else:
                #If there aren't moves, pass
                passCount += 1
            actualTurnPlayer = white if actualTurnPlayer is black else black
            self.board.passCount = passCount

    def train(self, num_episodes, dbGames=[]):
        """ Train othello game, run games for especified num_episodes
        @param int num_episodes
        @param list(list(int)) dbGames
        @return list(int,int) wins
        @return float time
        """
        start = timeit.default_timer()
        wins = []

        # Train #num_episodes
        for i in range(num_episodes):
            dbGame = []
            if dbGames:
                dbGame = dbGames[i]
            self.gameStart(i,dbGame)

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
        time = str(stop-start)
        return wins,time

    def play(self,num_episodes):
        """ Play othello game, run games for especified num_episodes
        @param int num_episode
        @return list(int,int) wins
        @return float time
        """
        start = timeit.default_timer()
        winB = winW = 0
        wins = []

        # Play #num_episodes
        for i in range(num_episodes):
            self.gameStart(i)

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
        time = str(stop-start)
        print "Black wins: " + str(winB/num_episodes*100) + "% - White wins: " + str(winW/num_episodes*100) + "%"
        return wins,time

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
            self.gameStart(i)

            if self.b.getScore(self.board) > self.w.getScore(self.board):
                winB += 1
            elif self.b.getScore(self.board) < self.w.getScore(self.board):
                winW += 1
        print "Black wins: " + str(winB) + "% - White wins: " + str(winW) + "%"
        print "---------------------------------------"
        self.b = tempB
        self.w = tempW
        return winB,winW

    def loadGames(self, db_path, num_episodes):
        """ Load professional saved games
        @param String db_path
        @param int num_episodes
        @return list(int,int) wins
        @return float time
        """
        filenames = ["originalDB","mirrorHDB","mirrorDDB","mirrorDHDB"]
        dbGames = []
        for filename in filenames:
            games,num_episodes = self.loadGame(db_path,filename,num_episodes)
            if games:
                dbGames += games
        return self.train(num_episodes,dbGames)

    def loadGame(self,db_path,filename,total_episodes):
        if total_episodes > 0:
            games = []
            with open(db_path+filename, 'r') as f:
                #Open file and read all
                lines = f.readlines()
                lines = [ line.strip() for line in lines ]
                num_episodes = total_episodes
                if num_episodes > len(lines):
                    num_episodes = len(lines)
                for idx in range(num_episodes):
                    newLine = eval(lines[idx])
                    games.append(newLine)
            total_episodes = total_episodes - len(games)
            return games, total_episodes
        return None,-1
