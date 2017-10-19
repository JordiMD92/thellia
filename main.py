#!/usr/bin/env python
from othello.game import Game
from othello.qtrainer import QTrainer
from players.humanplayer import HumanPlayer
from players.randomplayer import RandomPlayer
from players.qplayer import QPlayer
from views.consoleview import ConsoleView
from collections import deque

def loadGames(db):
    with open(db+"/db","r") as f:
        lines = f.readlines()
        lines = [deque(line.strip()) for line in lines]
        newLines = []
        for line in lines:
            newLine = []
            while line:
                c=line.popleft()
                r=line.popleft()
                move = (ord(c)-97)+(int(r)-1)*8
                newLine.append(move)
            newLines.append(newLine)
    return newLines

# Use a view and board
view = ConsoleView()
game = Game()
gamesDB = []

# Load DB to memory
if view.loadGames():
    gamesDB = loadGames("DB")

gameMode = view.getGameMode(game)
if gameMode == game.GameMode['train']:
    #DQN vs Random
    load_model = view.loadModel()
    trainer = QTrainer(1,RandomPlayer(-1),gamesDB,view)
    trainer.run(load_model)
else:
    if gameMode == game.GameMode['hvh']:
        #Human vs Human
        game.addPlayer(HumanPlayer(1,view))
        game.addPlayer(HumanPlayer(-1,view))
    elif gameMode == game.GameMode['hvr']:
        #Human vs Random, ask tile and create players
        playerTile = view.getHumanTile()
        game.addPlayer(HumanPlayer(playerTile,view))
        game.addPlayer(RandomPlayer(-playerTile))
    elif gameMode == game.GameMode['rvr']:
        #Random vs Random
        game.addPlayer(RandomPlayer(1))
        game.addPlayer(RandomPlayer(-1))
    elif gameMode == game.GameMode['qvr']:
        #DQN vs Random
        load_model = view.loadModel()
        game.addPlayer(QPlayer(1,load_model))
        game.addPlayer(RandomPlayer(-1))
    elif gameMode == game.GameMode['qvh']:
        #DQN vs Random
        load_model = view.loadModel()
        game.addPlayer(QPlayer(1,load_model))
        game.addPlayer(HumanPlayer(-1,view))
    #Run game
    game.run(view)
