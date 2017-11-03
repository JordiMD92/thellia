#!/usr/bin/env python
from os import listdir
from os.path import isfile, join
from xml.etree import cElementTree as ET
import struct

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

xmlParser()
wtbParser()
