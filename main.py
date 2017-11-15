#!/usr/bin/env python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
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

def gameMode(num_episodes,train,sess):
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
        return QPlayer(1,QN,train,num_episodes,sess), QPlayer(-1,QN,train,num_episodes,sess)
    elif gameMode == GameMode['qvh']:
        #DQN vs Human
        return QPlayer(1,QN,train,num_episodes,sess), HumanPlayer(-1,view)
    elif gameMode == GameMode['qvr']:
        #DQN vs Random
        return QPlayer(1,QN,train,num_episodes,sess), RandomPlayer(-1)

def loadDB(modelPath,model,sess):
    # Load DB to memory
    dbPath = "./DB/db"
    # Get num_episodes to load
    num_games = view.getNumEpisodes(True)
    if num_games:
        p1 = QPlayer(1,QN,"load",num_games,sess)
        p2 = QPlayer(-1,QN,"load",num_games,sess)
        dbGame = Game(MinimalView(),p1,p2,modelPath,sess)
        dbModel = dbGame.loadGames(dbPath,num_games)
        saver.save(sess,dbModel+'/model-'+str(num_games)+'.ckpt')
        renameFolder(modelPath,dbModel)

def train(view,modelPath,sess):
    # Get num_episodes to train
    num_episodes = view.getNumEpisodes()
    # Create game and add players
    p1,p2 = gameMode(num_episodes,True,sess)
    game = Game(view,p1,p2,modelPath,sess)
    print "Game Running..."
    end_model = game.train(num_episodes)
    saver.save(sess,end_model+'/model-'+str(num_episodes)+'.ckpt')
    renamed_model = renameFolder(modelPath,end_model)
    pr.printPlot(renamed_model)

def play(view,modelPath,sess):
    # Get num_episodes to play
    num_episodes = view.getNumEpisodes()
    # Create game and add players
    p1,p2 = gameMode(num_episodes,False,sess)
    game = Game(view,p1,p2,modelPath,sess)
    print "Game Running..."
    end_model = game.play(num_episodes)
    renamed_model = renameFolder(modelPath,end_model)
    pr.printPlot(renamed_model)

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

# Initialize Session
init = tf.global_variables_initializer()
saver = tf.train.Saver()

#Ask what mode want to run 'loadDB, train or play'
mode = view.getMode()
# ASk if want to load saved model
model = view.loadModel(modelPath)

with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
#with tf.Session() as sess:
    sess.run(init)

    if model:
        print "Loading Model: "+model
        ckpt = tf.train.get_checkpoint_state(model)
        saver.restore(sess,ckpt.model_checkpoint_path)

    if mode == "load":
        loadDB(modelPath,model,sess)
    elif mode == "train":
        train(view,modelPath,sess)
    elif mode == "play":
        play(view,modelPath,sess)

print "Application finalized"
