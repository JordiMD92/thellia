import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class ProcessResults():

    def __init__(self):
        self.fn = "/results"

    def saveResults(self,results,time,model_path,mode):
        print results
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
            if mode == "play\n":
                print lines[3]
            else:
                winsMTB = lines[3].split(":")
                winsMTW = lines[4].split(":")
                winsMTB = map(float, winsMTB)
                winsMTW = map(float, winsMTW)
                print lines[5]
        winsB = map(float, winsB)
        winsW = map(float, winsW)
        print "Mitjana Random- Black: "+str((sum(winsB)/len(winsB)))+" % - White: "+str((sum(winsW)/len(winsW)))+" %"
        if mode != "play\n":
            print "Mitjana MaxTile- Black: "+str((sum(winsMTB)/len(winsMTB)))+" % - White: "+str((sum(winsMTW)/len(winsMTW)))+" %"
        plt.figure(1)
        plt.plot([x for x in winsB],'r^',[y for y in winsW],'bs')
        plt.axis([0, len(winsB)-1, 0, 100])
        black = mlines.Line2D([], [], color='red', marker='^', markersize=15, label='Black Wins')
        white = mlines.Line2D([], [], color='blue', marker='s', markersize=15, label='White Wins')
        plt.legend(handles=[black,white])
        plt.show()
