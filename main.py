#!/usr/bin/env python
import os, sys, getopt, errno
from othello.game import Game
from views.minimalview import MinimalView
from players.humanplayer import HumanPlayer
from players.randomplayer import RandomPlayer
from players.qplayer import QPlayer
from networks.qnetwork_sigmoid import QNetworkSigmoid
from networks.qnetwork_relu import QNetworkRelu
from othello.process_results import ProcessResults

""" page 105-145, 229-313, 439-473 | 40+84+34 = 158
lr <- grid search """

model_path = "./models"
db_path = "./DB/db"
view = MinimalView()
pr = ProcessResults()

def getArgs(argv):
    """ Get arguments, check values and parse
    @return String mode
    @return int num_episodes
    @return QNetwork QN
    @return Player b
    @return Player w
    @return String load
    """
    num_episodes = 0
    mode = qn_arg = b_arg = w_arg = load = ""
    try:
        opts,args = getopt.getopt(argv,'m:e:n:b:w:l:',['mode=','episodes=','neural_network=','black=','white=','load='])
    except getopt.GetoptError as err:
        usage("Bad arguments usage")
    for opt, arg in opts:
        if opt in ("-m","--mode"):
            if arg not in ("play","train","load"):
                usage(arg+" is not a mode")
            mode = arg
        if opt in ("-e","--episodes"):
            try:
                if int(arg) >= 1:
                    num_episodes = int(arg)
                else:
                    raise Exception()
            except Exception as e:
                print "The number of episodes must be a positive integer"
        if opt in ("-n","--neural_network"):
            if arg not in ("relu","sigmoid"):
                usage(arg+" is not a compatible network")
            qn_arg = arg
        if opt in ("-b","--black"):
            if arg not in ("QP","RP","HP",""):
                usage(arg+" is not a compatible player")
            b_arg = arg
        if opt in ("-w","--white"):
            if arg not in ("QP","RP","HP",""):
                usage(arg+" is not a compatible player")
            w_arg = arg
        if opt in ("-l","--load"):
            load = arg

    if mode == "" or num_episodes == 0 or qn_arg == "":
        usage("Mode, number of episodes and neural network are needed")
    if mode in ("play","train") and b_arg == "" and w_arg == "":
        print "Players are needed to " + mode
        sys.exit(2)

    if qn_arg == "relu":
        QN = QNetworkRelu()
    if qn_arg == "sigmoid":
        QN = QNetworkSigmoid()

    if mode == "load":
        b = QPlayer(1,QN,mode,num_episodes)
        w = QPlayer(-1,QN,mode,num_episodes)
    else:
        b = HumanPlayer(1,view)
        if b_arg == "RP":
            b = RandomPlayer(1)
        elif b_arg == "QP":
            b = QPlayer(1,QN,mode,num_episodes)
        w = HumanPlayer(-1,view)
        if w_arg == "RP":
            w = RandomPlayer(-1)
        elif w_arg == "QP":
            w = QPlayer(-1,QN,mode,num_episodes)

    try:
        os.makedirs(model_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    if load:
        if qn_arg not in load:
            print "That network is not compatible with that model"
            sys.exit(2)
        folders = os.walk(model_path).next()[1]
        if load not in folders:
            print "You must type a valid folder from models"
            sys.exit(2)
        else:
            QN.loadModel(model_path+"/"+load)
            print "Model ["+load+"] loaded"

    return mode,num_episodes,QN,b,w,load

def usage(error):
    """ Print information and exit """
    print error
    print "main.py -m <mode> -e <num_episodes> -n <neural_network> -b <player1_type> -w <player2_type> -l <load_model>"
    print "<mode>: [train/play/load] (train game, play game, or load from db)"
    print "<neural_network>: [relu,sigmoid]"
    print "<player_type>: [QP/RP/HP] (QPlayer, RandomPlayer, HumanPlayer)"
    sys.exit(2)

def getModel_name(mode, num_episodes, QN, b, w, load_model):
    """ Get model name of the folders
    @param String mode
    @param int num_episodes
    @param QNetwork QN
    @param Player b
    @param Player w
    @param String load_model
    @return String model_name
    """
    if num_episodes % 1000000 == 0:
        str_num_episodes = str(num_episodes/1000000)+"M"
    elif num_episodes % 1000 == 0:
        str_num_episodes = str(num_episodes/1000)+"k"
    else:
        str_num_episodes = str(num_episodes)
    model_name = mode +"_"+ str_num_episodes +"_"+ QN.getType() +"_b"+ b.getType()+"_w"+ w.getType()
    if load_model:
        model_name += "_("+load_model+")"
    return model_name

def save_model(model_name,results,QN,i):
    """ Save model and results
    @param String model_name
    @param list(int,int) results
    @param QNetwork QN
    @param int i
    """
    new_model_name = model_name
    if i>0:
        new_model_name = model_name+"_"+str(i)
    if os.path.exists(model_path+"/"+new_model_name):
        save_model(model_name,results,QN,i+1)
    else:
        try:
            os.makedirs(model_path+"/"+new_model_name)
            pr.saveResults(results,model_path+"/"+new_model_name)
            QN.saveModel(model_path+"/"+new_model_name)
            print "Model saved as: "+new_model_name
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

def main(argv):
    # Use view and initalize game and QNetwork
    mode, num_episodes, QN, b, w, load_model = getArgs(argv)
    model_name = getModel_name(mode,num_episodes, QN, b, w, load_model)

    game = Game(view,b,w)
    if mode == "load":
        results = game.loadGames(db_path, num_episodes)
    elif mode == "train":
        results = game.train(num_episodes)
    elif mode == "play":
        results = game.play(num_episodes)

    save_model(model_name, results, QN, 0)
    print "Application finalized"

if __name__ == "__main__":
   main(sys.argv[1:])
