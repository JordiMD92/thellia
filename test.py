#!/usr/bin/env python
from othello.game import Game
from othello.player import Player
from views.consoleview import ConsoleView

#Use a view and board
view = ConsoleView()
game = Game()

#Human vs Human
game.addPlayer(Player(1))
game.addPlayer(Player(-1))

#Human vs Computer, ask tile and create players
#playerTile = view.initMsg()
#game.addPlayer(Player(playerTile))
#game.addPlayer(Player(-playerTile))

#Run game
game.run(view)
