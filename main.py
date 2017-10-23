#!/usr/bin/env python
from othello.game import Game
from views.consoleview import ConsoleView
from views.minimalview import MinimalView
from players.humanplayer import HumanPlayer
from players.randomplayer import RandomPlayer
from players.qplayer import QPlayer
from othello.qnetwork import QNetwork

# Use view and initalize game
dqnPath = "./dqn"
view = MinimalView()
game = Game(view,dqnPath)
QN = QNetwork(0.01)

gameMode = view.getGameMode(game)
if gameMode == game.GameMode['hvh']:
    #Human vs Human
    p1 = HumanPlayer(1,view)
    p2 = HumanPlayer(-1,view)
elif gameMode == game.GameMode['hvr']:
    #Human vs Random, ask tile and create players
    playerTile = view.getHumanTile()
    p1 = HumanPlayer(playerTile,view)
    p2 = RandomPlayer(-playerTile)
elif gameMode == game.GameMode['rvr']:
    #Random vs Random
    p1 = RandomPlayer(1)
    p2 = RandomPlayer(-1)
elif gameMode == game.GameMode['qvq']:
    #DQN vs DQN
    p1 = QPlayer(1,QN)
    p2 = QPlayer(-1,QN)
elif gameMode == game.GameMode['qvh']:
    #DQN vs Human
    p1 = QPlayer(1,QN)
    p2 = HumanPlayer(-1,view)
elif gameMode == game.GameMode['qvr']:
    #DQN vs Random
    p1 = QPlayer(1,QN)
    p2 = RandomPlayer(-1)

# Train AI
num_episodes = 1
train = False
load_model = False
if gameMode >= 4:
    # Load DB to memory
    load_episodes = view.loadGames()
    if load_episodes:
        print "Loading games..."
        gamesDB,load_episodes = game.loadGames("DB/db",load_episodes)
        game.setView(MinimalView())
        game.addPlayers(p1,p2)
        game.run(load_episodes,False,gamesDB)
        p1,p2 = game.getPlayers()
        game = Game(MinimalView(),dqnPath)

    train, num_episodes = view.isTrainning()
    p1.setTrain(train)
    p2.setTrain(train)

    load_model = view.loadModel()

game.addPlayers(p1,p2)
game.setView(view)

#Run game
print "Game Running..."
game.run(num_episodes,load_model)
