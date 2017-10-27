#!/usr/bin/env python
import os
from othello.process_results import ProcessResults

# Parse games XML and WTHOR to single file
def loadModel(path):
    """ Ask if want to load DQN trained model """
    print("Wich model do you want to load?")
    models = os.walk(path).next()[1]
    i = 0
    for model in models:
        i+=1
        print "["+str(i)+"] "+model
    while True:
        load_model = raw_input("Type [0] not to load, otherwise > 1: ")
        try:
            if int(load_model) == 0:
                return False
            elif int(load_model) > 0 and int(load_model) <= len(models):
                return models[int(load_model)-1]
            print("Invalid input, try again")
        except:
            print("Invalid input, try again")
    return


pr = ProcessResults()
modelPath = "./models"
model = loadModel(modelPath)
if model:
    path = modelPath+"/"+model
    pr.printPlot(path)
else:
    print "No model loaded"
