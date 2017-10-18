#!/usr/bin/env python
from othello.game import Game
from othello.qtrainer import QTrainer
from players.humanplayer import HumanPlayer
from players.randomplayer import RandomPlayer
from views.consoleview import ConsoleView
#from othello.qtable import QTable

#Use a view and board
view = ConsoleView()
game = Game()
gameMode = game.GameMode['train']
load_model = False
#gameMode = view.getGameMode(game)
if gameMode == game.GameMode['train']:
    #DQN vs Random
    trainer = QTrainer(1,RandomPlayer(-1),view)
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
        game.addPlayer(QPlayer(1))
        game.addPlayer(RandomPlayer(-1))
    #Run game
    game.run(view)
