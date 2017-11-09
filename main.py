#!/usr/bin/env python
import os
from othello.game import Game
from views.consoleview import ConsoleView
from views.minimalview import MinimalView
from players.humanplayer import HumanPlayer
from players.randomplayer import RandomPlayer
from players.qplayer import QPlayer
from othello.qnetwork_64 import QNetwork64
from othello.qnetwork_129 import QNetwork129
from othello.qnetwork_relu import QNetworkRelu
from othello.process_results import ProcessResults

""" page 105-145, 229-313, 439-473 | 40+84+34 = 158 """

def gameMode(game):
    gameMode = view.getGameMode(game)
    if gameMode == game.GameMode['hvh']:
        #Human vs Human
        return HumanPlayer(1,view),HumanPlayer(-1,view)
    elif gameMode == game.GameMode['hvr']:
        #Human vs Random, ask tile and create players
        playerTile = view.getHumanTile()
        return HumanPlayer(playerTile,view), RandomPlayer(-playerTile)
    elif gameMode == game.GameMode['rvr']:
        #Random vs Random
        return RandomPlayer(1), RandomPlayer(-1)
    elif gameMode == game.GameMode['qvq']:
        #DQN vs DQN
        return QPlayer(1,QN), QPlayer(-1,QN)
    elif gameMode == game.GameMode['qvh']:
        #DQN vs Human
        return QPlayer(1,QN), HumanPlayer(-1,view)
    elif gameMode == game.GameMode['qvr']:
        #DQN vs Random
        return QPlayer(1,QN), RandomPlayer(-1)

def loadDB(dbPath,view,modelPath):
    # Load DB to memory
    num_games = view.loadGames()
    if num_games:
        dbGame = Game(MinimalView(),modelPath)
        dbGame.addPlayers(QPlayer(1,QN),QPlayer(-1,QN))
        dbModel = dbGame.loadGames(dbPath,num_games)
        print "DB saved on: " + dbModel

def loadModel(modelPath):
    return view.loadModel(modelPath)

# Use view and initalize game and QNetwork
num_episodes = 1
modelPath = "./models"
dbPath = "./DB/db"
view = MinimalView()
QN = QNetwork64(0.001)
pr = ProcessResults()

# Load db games
loadDB(dbPath,view,modelPath)

# Create game and add players
game = Game(view,modelPath)
p1,p2 = gameMode(game)
game.addPlayers(p1,p2)

# ASk if want to load saved model
model = loadModel(modelPath)

# Get num_episodes to train
num_episodes = view.getTrainEpisodes()

#Run game
if num_episodes > 0:
    print "Game Running..."
    end_model = game.run(num_episodes,model)
    pr.printPlot(end_model)
print "Application finalized"
