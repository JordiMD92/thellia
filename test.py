#!/usr/bin/env python
from othello.game import Game
from othello.humanplayer import HumanPlayer
from othello.randomplayer import RandomPlayer
from views.consoleview import ConsoleView

#Use a view and board
view = ConsoleView()
game = Game()

gameMode = view.getGameMode(game)
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

#Run game
game.run(view)
