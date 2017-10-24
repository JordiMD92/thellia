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

def gameMode():
    gameMode = view.getGameMode(game)
    if gameMode == game.GameMode['hvh']:
        #Human vs Human
        return HumanPlayer(1,view),HumanPlayer(-1,view),gameMode
    elif gameMode == game.GameMode['hvr']:
        #Human vs Random, ask tile and create players
        playerTile = view.getHumanTile()
        return HumanPlayer(playerTile,view), RandomPlayer(-playerTile),gameMode
    elif gameMode == game.GameMode['rvr']:
        #Random vs Random
        return RandomPlayer(1), RandomPlayer(-1),gameMode
    elif gameMode == game.GameMode['qvq']:
        #DQN vs DQN
        return QPlayer(1,QN), QPlayer(-1,QN),gameMode
    elif gameMode == game.GameMode['qvh']:
        #DQN vs Human
        return QPlayer(1,QN), HumanPlayer(-1,view),gameMode
    elif gameMode == game.GameMode['qvr']:
        #DQN vs Random
        return QPlayer(1,QN), RandomPlayer(-1),gameMode

def loadDB(dbPath,game):
    # Load DB to memory
    num_games = view.loadGames()
    if num_games:
        game.setView(MinimalView())
        game.addPlayers(QPlayer(1,QN),QPlayer(-1,QN))
        dbModel = game.loadGames(dbPath,num_games)
        print "DB saved on: " + dbModel

def loadModel(modelPath):
    return view.loadModel(modelPath)

# Use view and initalize game and QNetwork
num_episodes = 1
modelPath = "./models"
dbPath = "./DB/db"
view = MinimalView()
game = Game(view,modelPath)
QN = QNetwork64(0.001)

p1,p2,gameMode = gameMode()
print ""
loadDB(dbPath,game)
print ""
game = Game(view,modelPath)
game.addPlayers(p1,p2)
model = loadModel(modelPath)
print ""
num_episodes = view.getTrainEpisodes()
print ""
game.setView(view)

#Run game
if num_episodes > 0:
    print "Game Running..."
    game.run(num_episodes,model)
print "Application finalized"
