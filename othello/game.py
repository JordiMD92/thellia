from __future__ import division
import timeit
import time
from othello.board import Board
from players.randomplayer import RandomPlayer
from players.maxtileplayer import MaxTilePlayer

class Game:

	def __init__(self, view, b, w):
		self.view = view
		self.b = b
		self.w = w
		self.board = Board()

	def reset(self):
		""" Reset environment
		@return Player,int,int actualTurnPlayer,passCount,idx
		"""
		self.board = Board()
		return self.b,0,0

	def gameStart(self, dbGame=[]):
		""" Game engine to play Othello, switch between players and do moves
		@param list(int) dbGame
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

	def next(self,board,action,tile):
		"""Get next possible state from actual state and action
		@param Board board
		@param int action
		@param int tile
		@return Board,int,bool nextState,r,done
		"""
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
				nextBoard,_,_ = tempBoard.next(move,opponent.getTile())
				return nextBoard.getBoardState(),r,done
		return tempBoard.getBoardState(),r,done

	def testTraining(self):
		""" Play one game against RandomPlayer and MaxTilePlayer
		@return list[float][float],list[float][float] winMT,winR
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
		@return list(int,int) wins
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
				winMT = (winMTB/100,winMTW/100)
				winR = (winRB/100,winRW/100)
				wins.append((winMT,winR))
				winsBatch = []
				winMTB = winMTW = winRB = winRW = 0
				print "{"+str(i+1)+" - "+str(num_episodes)+"} - Black: "+str(winR[0])+"% - White: "+str(winR[1]) + "%"
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
			self.gameStart()

			# Save wins and show time
			if i % 100 == 0 and i > 0 and i != num_episodes:
				wins.append(((winB/i*100),(winW/i*100)))
			if i % 1000 == 0 and i > 0 and i != num_episodes:
				print "("+str(i)+") Black wins: " + str(winB/i * 100) + "% - White wins: " + str(winW/i * 100) + "%"
				print "Temps: " + str(timeit.default_timer()-start)

			if self.b.getScore(self.board) > self.w.getScore(self.board):
				winB += 1
			elif self.b.getScore(self.board) < self.w.getScore(self.board):
				winW += 1

		# Save wins and show time
		wins.append(((winB/num_episodes*100),(winW/num_episodes*100)))
		time = str(timeit.default_timer()-start)
		if num_episodes != 1:
			print "Black wins: " + str(winB/num_episodes*100) + "% - White wins: " + str(winW/num_episodes*100) + "%"
		return wins,time

	def loadGames(self, db_path, total_episodes):
		""" Load professional saved games
		@param String db_path
		@param int num_episodes
		@return list(int,int) wins
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
