import shutil
import os
import os.path
import struct
from kh2rando_binUtils import openKHBinFile,findHeaderinBAR,findBarHeader

from utils import writeRandomizationLog, readHex, readHexPure, readAndUnpack, fileByteToHexToList, writeIntOrHex,copyKHFile,PS3Version

def setSoraPartyMembers(doItOrNot):
    #set roxas and kh1 sora to kh2 sora
    if doItOrNot:
        print("Replacing sora party members...")
        fileBin = openKHBinFile("03system.bin")
        if (fileBin):
            Offset = findBarHeader(fileBin)
            fileBin.seek(0x15904+Offset, 0)  # skip to roxas thingy
            writeIntOrHex(fileBin, 0x54, 2) #Write kh2 sora ucm code
            fileBin.seek(0x1596c+Offset, 0)  # skip to kh1 sora
            writeIntOrHex(fileBin, 0x54, 2) #Write kh2 sora ucm code
            fileBin.seek(0x15938+Offset, 0)  # skip to dual weilded roxas
            writeIntOrHex(fileBin, 0x54, 2) #Write kh2 sora ucm code
            print("Done!")
            fileBin.close()
def skipGummiShipMissions(doItOrNot):
    #set roxas and kh1 sora to kh2 sora
    if doItOrNot:
        print("Skipping gummiship missions...")
        if copyKHFile("00progress.bin"):
            fileBin = open("00progress.bin",'rb+')
            if (fileBin):
                skipCode = [0x04,0x00, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00]
                findHeaderinBAR(fileBin,'wldf',True)
                if PS3Version():
                    skipCode.insert(0,0x00)
                fileBin.seek(0x9b4,1)
                fileBin.write(bytearray(skipCode))
                print("Done!")
                fileBin.close()

def skipCredits(doItOrNot):
    #set roxas and kh1 sora to kh2 sora
    if doItOrNot:
        regionExtraFolder = ""
        if PS3Version():
            regionExtraFolder = "us/"
        filename = "ard/" + regionExtraFolder + 'eh20.ard'
        print("Skipping credits...")
        if copyKHFile(filename):
            fileBin = open(filename,'rb+')
            if (fileBin):
                #BytesToWrite =   01 40
                if not PS3Version():
                    fileBin.seek(0x7c0,0) #Go to map event location and change from 33 to 3C
                else:
                    fileBin.seek(0x7f8, 0)  # Diff spot in PS3 version

                writeIntOrHex(fileBin,1,2) #
                writeIntOrHex(fileBin,0,2) #
                writeIntOrHex(fileBin,0x05,2) #
                writeIntOrHex(fileBin,1,2) #
                writeIntOrHex(fileBin,0,2) #
                writeIntOrHex(fileBin,0,2) #
                writeIntOrHex(fileBin,5,2) #
                writeIntOrHex(fileBin,0x4001,2) #
                print("Done!")
                fileBin.close()
def giveHUDElements():
    pass #Don't do this for now, it sets all battle levels of worlds to lvl 1 which makes things too easy.
    """ progressBin data
    bar file inside bar file == so it has its own header with positions and such 
    0C ?? ?? ?? == Plays or starts a event of some kind? Always starts with 0C. May have something like a prefix
    0C 01 91 08 -- Start playing as KH1 Sora
    01 == Event Type? 01 or 02 and sometimes 0?
    91 == Event ID
    
    These event Id's dont show up anywhere else i can find ATM so i have no idea on how to manipluate these into not removing the hud elements
    These events when triggered also seem to affect the save data part of RAM 
    """
    print("Giving hud elements early...")
    if copyKHFile("00progress.bin"):
        fileBin = open("00progress.bin",'rb+')
        if (fileBin):
            hudCode = [0x00]
            findHeaderinBAR(fileBin,'tt',True)
            fileBin.seek(0x6fa,1)
            fileBin.write(bytearray(hudCode))
            fileBin.close()
            print("Done!")
