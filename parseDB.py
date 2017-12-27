#!/usr/bin/env python
from os import listdir
from os.path import isfile, join
from xml.etree import cElementTree as ET
import struct
from othello.board import Board
from players.randomplayer import RandomPlayer

# Parse games XML and WTHOR to single file
def xmlParser():
    saveFile = open("DB/db","a")
    onlyfiles = [f for f in listdir("xml") if isfile(join("xml/", f))]
    for fname in onlyfiles:
        fullname = "xml/"+fname
        print fullname
        tree = ET.ElementTree(file=fullname)
        for elem in tree.iter(tag='moves'):
            saveFile.write(elem.text+"\n")
    saveFile.close()

def wtbParser():
    onlyfiles = [f for f in listdir("wtb") if isfile(join("wtb/", f))]
    saveFile = open("DB/db","a")
    fileHeaderLength = 16
    gameHeaderLength = 8
    numberOfPlays = 60
    gameBlockLength = gameHeaderLength + numberOfPlays

    for fname in onlyfiles:
        fullname = "wtb/"+fname
        print fullname
        with open(fullname,"rb") as f:
            byteFile = f.read()
            idx = fileHeaderLength
            while idx < len(byteFile):
                for playIdx in range(numberOfPlays):
                    play = byteFile[idx+gameHeaderLength+playIdx]
                    play = struct.unpack("B",play)[0]
                    if play > 0:
                        chars = str(play)
                        r,c = str(unichr(ord(chars[0]) + 48)), chars[1]
                        saveFile.write(r+c)
                saveFile.write("\n")
                idx += gameBlockLength
    saveFile.close()

def transformToDic():
    dbGames = []
    with open("DB/db","r") as f:
        #Open file and read all
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        for idx in range(len(lines)):
            # Put on memory only the number of games to play and return
            newLine = []
            i = 1
            for char in lines[idx]:
                if i % 2 == 0 and i > 0:
                    move = ord(preChar) - 97 + (int(char) - 1) * 8
                    newLine.append(move)
                else:
                    preChar = char
                i += 1
            dbGames.append(newLine)

    black = RandomPlayer(1)
    white = RandomPlayer(-1)
    splitGames = []
    for dbGame in dbGames:
        actualTurnPlayer = black
        board = Board()
        passCount = 0
        idx = 0
        splitGame = []
        while board.getRemainingPieces() > 0 and passCount < 2:
            possibleMoves = actualTurnPlayer.checkMoves(board)
            if possibleMoves:
                splitGame.append([])
                passCount = 0
                try:
                    move = dbGame[60 - board.getRemainingPieces()]
                except:
                    break
                board.updateBoard(actualTurnPlayer.getTile(), move)
                splitGame[idx].append(actualTurnPlayer.getTile())
                splitGame[idx].append(move)
                idx += 1
            else:
                passCount += 1
            actualTurnPlayer = white if actualTurnPlayer is black else black
        splitGames.append(splitGame)

    with open("DB/newDB","a") as fw:
        for game in splitGames:
            fw.write(str(game)+"\n")

def generateMirrorHGame():
    db_path = "DB/mirrorDDB"
    dbGames = []
    with open(db_path, 'r') as f:
        #Open file and read all
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        num_episodes = len(lines)
        for idx in range(num_episodes):
            newLine = eval(lines[idx])
            dbGames.append(newLine)

    idx = 0
    while idx < len(dbGames):
        idy = 0
        while idy < len(dbGames[idx]):
            dbGames[idx][idy][1] = 63 - dbGames[idx][idy][1]
            idy += 1
        idx += 1

    with open("DB/mirrorDHDB","a") as fw:
        for game in dbGames:
            fw.write(str(game)+"\n")


def generateMirrorDGame():
    db_path = "DB/originalDB"
    dbGames = []
    with open(db_path, 'r') as f:
        #Open file and read all
        lines = f.readlines()
        lines = [ line.strip() for line in lines ]
        num_episodes = len(lines)
        for idx in range(num_episodes):
            newLine = eval(lines[idx])
            dbGames.append(newLine)

    idx = 0
    while idx < len(dbGames):
        idy = 0
        while idy < len(dbGames[idx]):
            f = dbGames[idx][idy][1] / 8
            c = dbGames[idx][idy][1] % 8
            dbGames[idx][idy][1] = c * 8 + f
            idy += 1
        idx += 1


    with open("DB/mirrorDDB","a") as fw:
        for game in dbGames:
            fw.write(str(game)+"\n")

#xmlParser()
#wtbParser()
#transformToDic()
#generateMirrorHGame()
#generateMirrorDGame()
