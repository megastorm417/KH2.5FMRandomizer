import shutil
import os
import os.path
import random
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack, readHex, writeIntOrHex,copyKHFile,getGameVersion,PS3Version
#Problem = The header can mess up the positioning of the sub-file.
def findBarHeader(fileOpened):
    #This is mainly used for the PS3 version where the bar header can be offsetted by some random extra data.
    # We will use this in place of navigating to the start of every file.
    string = "BAR"
    fileOpened.seek(0, 0)
    test = string.encode('utf-8') +b'\01'
    dataRead = fileOpened.read()
    fileOpened.seek(0, 0)
    if test in dataRead:
        # find header thing
        newBarPos = dataRead.find(test)
        fileOpened.seek(newBarPos, 0)
        return newBarPos
    else:
        return False
def ReverseEndianString(string, size=2,reverseString = False,goingToEndian= False):
    if PS3Version():
        if goingToEndian:
            if len(string) % 2 == 1:
                string += '\x00'  # Keep even for reverse endian strings.
        if reverseString:
            string = string[len(string)::-1]
        return "".join(reversed([string[i:i+size] for i in range(0, len(string), size)]))
    else:
        return string

def openKHBinFile(filename,seekHex=0):
    """Open kh2 bin file and navigate to the start from the bar
        return a list/array of the file thing we opened and data like position and entry size"""
    if (copyKHFile(filename)):
        fileBin = open(filename, "rb+")
        if (fileBin):
            writeRandomizationLog(filename)
            FilePositionOfNew = 0
            FilePositionEntrySize = 0
            if(seekHex != 0):
                fileBin.seek(seekHex, 0)  #usually a bar name thing
                FilePositionOfNew = readAndUnpack(fileBin, 4);
                FilePositionEntrySize = readAndUnpack(fileBin, 4)
                fileBin.seek(FilePositionOfNew, 0)
            return fileBin
        else:
            ErrorWindow(
                "The file " + filename +"  could not be opened. It's probably in use by another program or instance of this program.")
            return False
    else:
        ErrorWindow(
            filename + " does not exist in the export/KH2/ folder. Make sure nothing has gone wrong during the extraction.")
        return False
def findHeaderinBAR(fileOpened,string,navigateToNewPos):

    if PS3Version(): #if Ps3, flip string because of endians
        string = string[len(string)::-1]
    test = string.encode('utf-8')
    if PS3Version(): #if Ps3, add spacing to get to the start like on the ps2 version
        while len(test) < 4:
            test = b'\00' + test
    fileOpened.seek(findBarHeader(fileOpened),0)

    dataRead = fileOpened.read()
    if test in dataRead:
        # find header thing
        barheaderOffsetPos = findBarHeader(fileOpened)
        btlIndex = dataRead.find(test)
        fileOpened.seek(barheaderOffsetPos+btlIndex, 0)
        if navigateToNewPos:
            if not PS3Version():
                fileOpened.seek(4, 1)
            else:
                fileOpened.seek(len(test), 1)
            newPos = readAndUnpack(fileOpened, 4)
            fileOpened.seek(newPos+barheaderOffsetPos,0)
        return True
    else:
        return False
def ModifyExtraFilePosition(fileBin,position,secondPosition): #PS3 Version Only
    #Extra files are at the end of the normal bar file.
    if PS3Version():
        oldPos = fileBin.tell();
        fileBin.seek(4,0)
        amtOfExtraFileEntries = readAndUnpack(fileBin,4)
        for x in range(amtOfExtraFileEntries):
            fileBin.seek(0x10 + (x*0x30), 0)
            fileBin.seek(0x20, 1) #skip string
            extraFilePos = readAndUnpack(fileBin,4) #Read position
            offset = position-extraFilePos
            fileBin.seek(-4, 1)  # go back
            extraFilePos += offset
            writeIntOrHex(fileBin,extraFilePos,4)
            fileBin.write(b'\x20')
            writeIntOrHex(fileBin,secondPosition,3)
        fileBin.seek(oldPos,0)


    else:
        return False
def ModifyExtraFileNames(fileBin,oldFileName,NewfileName): #PS3 Version Only
    #Extra file names that are present in some files
    #If they aren't renamed, the game will fail to load them.
    if PS3Version():
        oldPos = fileBin.tell();
        fileBin.seek(4,0)
        amtOfExtraFileEntries = readAndUnpack(fileBin,4)
        for x in range(amtOfExtraFileEntries):
            fileBin.seek(0x10 + (x*0x30), 0)
            extraFileNameStr = fileBin.read(0x20).decode("UTF-8").rstrip('\x00')
            extraFileNameStr = extraFileNameStr.replace(oldFileName,NewfileName)
            fileBin.seek(0x10 + (x * 0x30), 0)
            emptyString = '\x00' * 20 #Clear out before writing so we dont miss any leftover bytes.
            fileBin.write(emptyString.encode("UTF-8"));
            fileBin.seek(0x10 + (x * 0x30), 0)
            fileBin.write(extraFileNameStr.encode("UTF-8"));
        fileBin.seek(oldPos,0)


    else:
        return False
def replaceAllStringInFile(fileBin,oldString,newString):
    oldString = oldString.encode('utf-8')
    newString = newString.encode('utf-8')
    oldPos = fileBin.tell()
    fileBin.seek(0, 0)
    alldata = fileBin.read()
    alldata.replace(oldString, newString)
    fileBin.seek(0, 0)
    fileBin.write(alldata)
    fileBin.seek(oldPos, 0)