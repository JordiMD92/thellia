#!/usr/bin/env python
import os, sys, getopt, errno
from othello.game import Game
from views.minimalview import MinimalView
from players.player_factory import PlayerFactory
from networks.qnetwork_factory import QNetworkFactory
from othello.process_results import ProcessResults

""" page 105-145, 229-313, 439-473 """

model_path = "./models"
db_path = "./DB/"
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
    num_episodes = batch_size = 0
    mode = qn_arg = b_arg = w_arg = load = ""
    #Check arguments
    try:
        opts,args = getopt.getopt(argv,'m:e:n:s:b:w:l:',['mode=','episodes=','neural_network=','batch_size=','black=','white=','load='])
    except getopt.GetoptError as err:
        usage("Bad arguments usage")
    for opt, arg in opts:
        #Check mode argument
        if opt in ("-m","--mode"):
            if arg not in ("play","train","load"):
                usage(arg+" is not a mode")
            mode = arg
        #Check episodes argument
        if opt in ("-e","--episodes"):
            try:
                if int(arg) > 0:
                    num_episodes = int(arg)
                else:
                    raise Exception()
            except Exception as e:
                print "The number of episodes must be a positive integer"
        #Check network argument
        if opt in ("-n","--neural_network"):
            if arg not in (QNetworkFactory.getTypes()):
                usage(arg+" is not a compatible network")
            qn_arg = arg
        #Check batch size
        if opt in ("-s","--batch_size"):
            try:
                if int(arg) > 0:
                    batch_size = int(arg)
                else:
                    raise Exception()
            except Exception as e:
                print "The number of batch size must be a positive integer"
        #Check black player argument
        if opt in ("-b","--black"):
            if arg not in (PlayerFactory.getTypes()):
                usage(arg+" is not a compatible player")
            b_arg = arg
        #Check white player argument
        if opt in ("-w","--white"):
            if arg not in (PlayerFactory.getTypes()):
                usage(arg+" is not a compatible player")
            w_arg = arg
        #Check load model argument
        if opt in ("-l","--load"):
            load = arg
    #Those 3 arguments are needed
    if mode == "" or num_episodes == 0 or qn_arg == "" or batch_size == 0:
        usage("Mode, number of episodes, neural network and batch size are needed")
    #If play or train, players are needed
    if mode in ("play","train") and b_arg == "" and w_arg == "":
        print "Players are needed to " + mode
        sys.exit(2)

    #Get QNetwork
    QN = QNetworkFactory.create(qn_arg,batch_size)

    #Get Players
    b,w = PlayerFactory.create(b_arg,w_arg,QN,mode,num_episodes)

    #Create model_path if doesn't exists
    try:
        os.makedirs(model_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    #Load model from model_path
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
    print "main.py -m <mode> -e <num_episodes> -n <neural_network> -s <batch_size> -b <player1_type> -w <player2_type> -l <load_model>"
    print "<mode>: [train/play/load] (train game, play game, or load from db)"
    print "<neural_network>: " + str(QNetworkFactory.getTypes())
    print "<player_type>: [QP/RP/HP] " + str(PlayerFactory.getTypes())
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
        str_num_episodes = str(int(num_episodes/1000000))+"M"
    elif num_episodes % 1000 == 0:
        str_num_episodes = str(int(num_episodes/1000))+"k"
    else:
        str_num_episodes = str(num_episodes)
    model_name = mode +"_"+ str_num_episodes +"_"+ QN.getType() +"_b"+ b.getType()+"_w"+ w.getType()
    if load_model:
        model_name += "_("+load_model+")"
    return model_name

def save_model(model_name,results,QN,time,i):
    """ Save model and results
    @param String model_name
    @param list(int,int) results
    @param QNetwork QN
    @param float time
    @param int i
    """
    new_model_name = model_name
    if i>0:
        new_model_name = model_name+"_"+str(i)
    if os.path.exists(model_path+"/"+new_model_name):
        save_model(model_name,results,QN,time,i+1)
    else:
        try:
            os.makedirs(model_path+"/"+new_model_name)
            pr.saveResults(results,time,model_path+"/"+new_model_name)
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
        results,time = game.loadGames(db_path, num_episodes)
    elif mode == "train":
        results,time = game.train(num_episodes)
    elif mode == "play":
        results,time = game.play(num_episodes)
    print "Temps Final: " + time

    save_model(model_name, results, QN, time, 0)
    print "Application finalized"

if __name__ == "__main__":
   main(sys.argv[1:])
