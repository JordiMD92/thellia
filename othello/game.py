from __future__ import division
import timeit
import time
import numpy as np
import tensorflow as tf
from othello.board import Board
from players.randomplayer import RandomPlayer
from players.maxtileplayer import MaxTilePlayer

class Game:

	def __init__(self, view, b, w, tbWriter):
		self.view = view
		self.b = b
		self.w = w
		self.board = Board()
		self.tbWriter = tbWriter

	def reset(self):
		""" Reset environment
		@return Player,int,int actualTurnPlayer,passCount,idx
		"""
		self.board = Board()
		return self.b,0,0

	def gameStart(self, dbGame=[]):
		""" Game engine to play Othello, switch between players and do moves
		@param list(int) dbGame
		@return int winner
		"""
		self.dbGame = dbGame
		# Reset board
		actualTurnPlayer,passCount,self.idx = self.reset()

		while not self.board.isEndGame():
			#If dbGame, check same tile turn. If not dbGame, get all possible moves
			possibleMoves = actualTurnPlayer.checkMoves(self.board, dbGame, self.idx)
			if possibleMoves:
				# If there is a move, get player move and update board
				passCount = 0
				self.idx += 1
				move = actualTurnPlayer.getMove(self, self.board, possibleMoves)
				self.board.updateBoard(actualTurnPlayer.getTile(), move)
			else:
				#If there aren't moves, pass
				passCount += 1
			actualTurnPlayer = self.w if actualTurnPlayer is self.b else self.b
			self.board.passCount = passCount
		return self.board.getWinner()

	def next(self,board,action,tile):
		"""Get next possible state from actual state and action
		@param Board board
		@param int action
		@param int tile
		@return Board,int,bool nextState,r,done
		"""
		possibleMoves = []
		move_maskPrime = np.zeros((64), dtype='float32')
		tempBoard,r,done = board.next(action,tile)
		if not done:
			opponent = self.b if self.b.getTile() != tile else self.w
			possibleMoves = opponent.checkMoves(tempBoard,self.dbGame,self.idx)
			if not possibleMoves:
				opponent = self.b if self.b.getTile() == tile else self.w
				possibleMoves = opponent.checkMoves(tempBoard,self.dbGame,self.idx)
			if possibleMoves:
				if opponent.getType() == "QP":
					tempTrain = opponent.train
					opponent.train = False
					move = opponent.getMove(self,tempBoard,possibleMoves)
					opponent.train = tempTrain
					opponent.conta -= 1
				else:
					move = opponent.getMove(self,tempBoard,possibleMoves)
				tempBoard,_,_ = tempBoard.next(move,opponent.getTile())
			move_maskPrime[possibleMoves] = 1
			tile = opponent.getTile()
		return tempBoard.getBoardState(tile),r,done,move_maskPrime

	def testTraining(self):
		""" Play one game against RandomPlayer and MaxTilePlayer
		@return list(list[float][float]) winMt+winR
		"""
		tempW = self.w
		tempBMode = self.b.mode
		self.w = MaxTilePlayer(-1)
		self.b.mode = "play"
		winMT,_ = self.play(1)
		self.w = RandomPlayer(-1)
		winR,_ = self.play(1)
		self.w = tempW
		self.b.mode = tempBMode
		return winMT+winR

	def train(self, num_episodes, dbGames=[]):
		""" Train othello game, run games for especified num_episodes
		@param int num_episodes
		@param list(list(int)) dbGames
		@return float time
		"""
		start = timeit.default_timer()
		wins = []
		winsBatch = []
		winMTB = winMTW = winRB = winRW = 0

		# Train #num_episodes
		for i in range(num_episodes):
			dbGame = []
			if dbGames:
				dbGame = dbGames[i]

			self.gameStart(dbGame)
			winsBatch.append(self.testTraining())

			# Save wins and show time
			if len(winsBatch) % 100 == 0 and i > 0:
				for winMT,winR in winsBatch:
					winMTB += winMT[0]
					winMTW += winMT[1]
					winRB += winR[0]
					winRW += winR[1]

				summary = tf.Summary(value=[tf.Summary.Value(tag="Wins MaxTile",simple_value=winMTB),])
				self.tbWriter.add_summary(summary)
				summary = tf.Summary(value=[tf.Summary.Value(tag="Wins Random",simple_value=winRB),])
				self.tbWriter.add_summary(summary)

				wins.append(((winMTB,winMTW),(winRB,winRW)))
				print "{"+str(i+1)+" - "+str(num_episodes)+"} - Black: "+str(winRB)+"% - White: "+str(winRW) + "%"
				winsBatch = []
				winMTB = winMTW = winRB = winRW = 0
			if i % 1000 == 0 and i > 0 and i != num_episodes:
				print "Temps: "+str(timeit.default_timer()-start)
		time = str(timeit.default_timer()-start)
		if wins:
			for winMT,winR in wins:
				winMTB += winMT[0]
				winMTW += winMT[1]
				winRB += winR[0]
				winRW += winR[1]
			print "\nMitjana partides Random - Black: "+str(winRB/len(wins))+"% - White: "+str(winRW/len(wins))+"%"
			print "Mitjana partides MaxTile - Black: "+str(winMTB/len(wins))+"% - White: "+str(winMTW/len(wins))+"%"
		return time

	def play(self,num_episodes):
		""" Play othello game, run games for especified num_episodes
		@param int num_episode
		@return list(int,int),float wins,time
		"""
		start = timeit.default_timer()
		winB = winW = 0
		wins = []

		# Play #num_episodes
		for i in range(num_episodes):
			winBlack,winWhite = self.gameStart()
			winB += winBlack
			winW += winWhite

			# Save wins and show time
			if (i+1) % 100 == 0 and i > 0 and i != num_episodes:
				wins.append(((winB),(winW)))
				print "{"+str(i+1)+" - "+str(num_episodes)+"} - Black wins: " + str(winB) + "% - White wins: " + str(winW) + "%"
				winB = winW = 0
			if (i+1) % 1000 == 0 and i > 0 and i != num_episodes:
				print "Temps: " + str(timeit.default_timer()-start)

		time = str(timeit.default_timer()-start)
		if wins:
			for win in wins:
				winB += win[0]
				winW += win[1]
			print "\nMitjana partides - Black: "+str(winB/len(wins))+"% - White: "+str(winW/len(wins))+"%"
		if num_episodes == 1:
			wins.append(((winB),(winW)))
		return wins,time

	def loadGames(self, db_path, total_episodes):
		""" Load from all professional saved games
		@param String db_path
		@param int num_episodes
		@return float time
		"""
		num_episodes = total_episodes
		filenames = ["originalDB","mirrorHDB","mirrorDDB","mirrorDHDB"]
		dbGames = []
		for filename in filenames:
			games,num_episodes = self.loadGame(db_path,filename,num_episodes)
			if games:
				dbGames += games
		train_episodes = total_episodes if num_episodes == -1 else total_episodes-num_episodes
		return self.train(train_episodes,dbGames)

	def loadGame(self,db_path,filename,total_episodes):
		"""
		Load professional saved games from a filename
		@param String db_path
		@param String filename
		@param int total_episodes
		@return list[games],int games,total_episodes
		"""
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
