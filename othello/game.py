from __future__ import division
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import timeit
import time
import tensorflow as tf
import board
import matplotlib.pyplot as plt

class Game:
    GameMode = {'hvh': 1,'hvr': 2,'rvr': 3,'qvq': 4,'qvh': 5,'qvr': 6}

    def __init__(self, view, path):
        self.view = view
        self.players = []
        self.board = board.Board()
        self.total_steps = 0

        self.gameModel = path+"/"+time.strftime("%Y-%m-%d_%H:%M:%S")
        #Make a path for our model to be saved in.
        if not os.path.exists(self.gameModel):
            os.makedirs(self.gameModel)

    def addPlayers(self, p1, p2):
        """ Add players to the game
        @param Player p1
        @param Player p2
        """
        self.players = []
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

    def run(self, num_episodes=1, load_model=False, gamesDB=[]):
        """ Run othello game, run games for especified num_episodes
        @param int num_episode
        @param list(list(int)) gamesDB
        """
        start = timeit.default_timer()
        winB = winW = 0
        wins = []
        init = tf.global_variables_initializer()
        try:
            saver = tf.train.Saver()
        except:
            pass
        with tf.Session() as sess:
            sess.run(init)

            if load_model:
                print "Loading Model: "+load_model
                ckpt = tf.train.get_checkpoint_state(load_model)
                saver.restore(sess,ckpt.model_checkpoint_path)
            # Set session for QPlayer
            self.players[0].setSessionEpisodes(sess,num_episodes)
            self.players[1].setSessionEpisodes(sess,num_episodes)

            for i in range(num_episodes):
                dbGame = []
                if gamesDB:
                    dbGame = gamesDB[i]
                self.reset()
                self.gameStart(dbGame)
                # Update buffers and e for QPlayer
                self.players[0].endGame()
                self.players[1].endGame()

                if i % 100 == 0 and i > 0:
                    wins.append(((winB/i*100),(winW/i*100)))
                if i % 1000 == 0 and i > 0:
                    saver.save(sess,self.gameModel+'/model-'+str(i)+'.ckpt')
                    print("Saved Model")
                    print "Black wins: " + str(winB/i * 100) + "% - White wins: " + str(winW/i * 100) + "%"
                    pause = timeit.default_timer()
                    print "Temps: " + str(pause-start)

                if self.getScore()[self.board.BLACK] > self.getScore()[self.board.WHITE]:
                    winB += 1
                elif self.getScore()[self.board.BLACK] < self.getScore()[self.board.WHITE]:
                    winW += 1
            try:
                saver.save(sess,self.gameModel+'/model-'+str(i)+'.ckpt')
                print "Model saved on: " + self.gameModel
            except:
                pass
        print "Black wins: " + str(winB/num_episodes*100) + "% - White wins: " + str(winW/num_episodes*100) + "%"
        stop = timeit.default_timer()
        print "Temps Final: " + str(stop-start)
        plt.figure(1)
        plt.subplot(111)
        plt.plot([x[0] for x in wins],'*')
        plt.axis([0, len(wins)-1, 0, 100])
        plt.show()
        #plt.subplot(112)
        #plt.plot([x[1] for x in wins],'*')
        #plt.axis([1, len(wins)-1, 0, 100])
        #plt.show()

    def gameStart(self, dbGame=[]):
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
                if dbGame:
                    try:
                        # If it is loading from DB, get next move
                        possibleMoves = [dbGame[60 - self.board.getRemainingPieces()]]
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
            self.run(load_episodes,False,newLines)
            return self.gameModel
