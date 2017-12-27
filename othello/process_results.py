import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.interpolate import interp1d
import numpy as np

class ProcessResults():

    def __init__(self):
        self.fn = "/results"

    def saveResults(self,results,time,model_path,mode):
        with open(model_path+self.fn,'w') as f:
            f.write(mode+"\n")
            winsB = []
            winsW = []
            winsMTB = []
            winsMTW = []
            if mode == "play":
                for elem in results:
                    winsB.append(elem[0])
                    winsW.append(elem[1])
                winsB = ':'.join(map(str, winsB))
                winsW = ':'.join(map(str, winsW))
                f.write(winsB+"\n")
                f.write(winsW+"\n")
            else:
                for winsMT,winsR in results:
                    winsB.append(winsR[0])
                    winsW.append(winsR[1])
                    winsMTB.append(winsMT[0])
                    winsMTW.append(winsMT[1])
                winsB = ':'.join(map(str, winsB))
                winsW = ':'.join(map(str, winsW))
                winsMTB = ':'.join(map(str, winsMTB))
                winsMTW = ':'.join(map(str, winsMTW))
                f.write(winsB+"\n")
                f.write(winsW+"\n")
                f.write(winsMTB+"\n")
                f.write(winsMTW+"\n")
            f.write("Temps: "+time+"\n")

    def printPlot(self,model):
        path = model+self.fn
        winsB = winsW = winsMTB = winsMTW = []
        with open(path, 'r') as f:
            #Open file and read all
            lines = f.readlines()
            mode = lines[0]
            winsB = lines[1].split(":")
            winsW = lines[2].split(":")
            winsB = map(float, winsB)
            winsW = map(float, winsW)
            if mode == "play\n":
                print lines[3]
            else:
                winsMTB = lines[3].split(":")
                winsMTW = lines[4].split(":")
                winsMTB = map(float, winsMTB)
                winsMTW = map(float, winsMTW)
                print lines[5]
        print "Mitjana Random - Black: "+str((sum(winsB)/len(winsB)))+" % - White: "+str((sum(winsW)/len(winsW)))+" %"
        if mode != "play\n":
            print "Mitjana MaxTile - Black: "+str((sum(winsMTB)/len(winsMTB)))+" % - White: "+str((sum(winsMTW)/len(winsMTW)))+" %"

        plt.figure(1)
        x = np.arange(0,len(winsB)*100,100)
        y = np.array(winsB)
        plt.plot(x,y)
        x2 = np.linspace(x.min(),x.max(),100)
        f = interp1d(x,y,kind='cubic')
        y2 = f(x2)
        #plt.plot(x2,y2)
        random = mlines.Line2D([], [], color='blue', label='Black Wins vs Random')
        maxTile = mlines.Line2D([], [], color='orange', label='Black Wins vs MaxTile')
        if mode != "play\n":
            y = np.array(winsMTB)
            plt.plot(x,y)
            f = interp1d(x,y,kind='cubic')
            y2 = f(x2)
            #plt.plot(x2,y2)
            plt.legend(handles=[random,maxTile])
        else:
            plt.legend(handles=[random])
        plt.show()
