import matplotlib.pyplot as plt
import matplotlib.lines as mlines

class ProcessResults():

    def __init__(self):
        self.fn = "/results"

    def saveResults(self,results,model_path):
        with open(model_path+self.fn,'w') as f:
            winsB = []
            winsW = []
            for elem in results:
                winsB.append(elem[0])
                winsW.append(elem[1])
            winsB = ':'.join(map(str, winsB))
            winsW = ':'.join(map(str, winsW))
            f.write(winsB+"\n")
            f.write(winsW+"\n")

    def printPlot(self,model):
        path = model+self.fn
        winsB = []
        winsW = []
        with open(path, 'r') as f:
            #Open file and read all
            lines = f.readlines()
            winsB = lines[0].split(":")
            winsW = lines[1].split(":")
        winsB = map(float, winsB)
        winsW = map(float, winsW)
        plt.figure(1)
        plt.plot([x for x in winsB],'r^',[y for y in winsW],'bs')
        plt.axis([0, len(winsB)-1, 0, 100])
        black = mlines.Line2D([], [], color='red', marker='^', markersize=15, label='Black Wins')
        white = mlines.Line2D([], [], color='blue', marker='s', markersize=15, label='White Wins')
        plt.legend(handles=[black,white])
        plt.show()
