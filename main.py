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

""" page 105-145, 229-313, 439-473 | 40+84+34 = 158
lr <- grid search """

def gameMode(num_episodes,train,):
    gameMode = view.getGameMode(GameMode)
    if gameMode == GameMode['hvh']:
        #Human vs Human
        return HumanPlayer(1,view),HumanPlayer(-1,view)
    elif gameMode == GameMode['hvr']:
        #Human vs Random, ask tile and create players
        playerTile = view.getHumanTile()
        return HumanPlayer(playerTile,view), RandomPlayer(-playerTile)
    elif gameMode == GameMode['rvr']:
        #Random vs Random
        return RandomPlayer(1), RandomPlayer(-1)
    elif gameMode == GameMode['qvq']:
        #DQN vs DQN
        return QPlayer(1,QN,train,num_episodes), QPlayer(-1,QN,train,num_episodes)
    elif gameMode == GameMode['qvh']:
        #DQN vs Human
        return QPlayer(1,QN,train,num_episodes), HumanPlayer(-1,view)
    elif gameMode == GameMode['qvr']:
        #DQN vs Random
        return QPlayer(1,QN,train,num_episodes), RandomPlayer(-1)

def loadDB(modelPath,model):
    # Load DB to memory
    dbPath = "./DB/db"
    # Get num_episodes to load
    num_games = view.getNumEpisodes(True)
    if num_games:
        p1 = QPlayer(1,QN,"load",num_games)
        p2 = QPlayer(-1,QN,"load",num_games)
        dbGame = Game(MinimalView(),p1,p2,modelPath)
        dbModel = dbGame.loadGames(dbPath,num_games)
        renamed_model = renameFolder(modelPath,dbModel)
        return renamed_model

def train(view,modelPath):
    # Get num_episodes to train
    num_episodes = view.getNumEpisodes()
    # Create game and add players
    p1,p2 = gameMode(num_episodes,True)
    game = Game(view,p1,p2,modelPath)
    print "Game Running..."
    end_model = game.train(num_episodes)
    renamed_model = renameFolder(modelPath,end_model)
    return renamed_model

def play(view,modelPath):
    # Get num_episodes to play
    num_episodes = view.getNumEpisodes()
    # Create game and add players
    p1,p2 = gameMode(num_episodes,False)
    game = Game(view,p1,p2,modelPath)
    print "Game Running..."
    end_model = game.play(num_episodes)
    renamed_model = renameFolder(modelPath,end_model)
    return renamed_model

def renameFolder(modelPath, model):
    new_name = ""
    while not new_name:
        new_name = raw_input("Type a name for this model: ")
        #TODO check directory doesn't exist
    os.rename(model,os.path.join(modelPath,new_name))
    return modelPath+"/"+new_name

# Use view and initalize game and QNetwork
GameMode = {'hvh': 1,'hvr': 2,'rvr': 3,'qvq': 4,'qvh': 5,'qvr': 6}
num_episodes = 1
modelPath = "./models"
view = MinimalView()
pr = ProcessResults()
QN = QNetworkRelu()

#Ask what mode want to run 'loadDB, train or play'
mode = view.getMode()
# ASk if want to load saved model
model = view.loadModel(modelPath)

if model:
    print "Loading Model: "+model
    QN.load_model(model)

if mode == "load":
    folder_model = loadDB(modelPath,model)
elif mode == "train":
    folder_model = train(view,modelPath)
elif mode == "play":
    folder_model = play(view,modelPath)

QN.save_model(folder_model)
pr.printPlot(folder_model)
print "Application finalized"
