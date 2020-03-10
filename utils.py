import ctypes
import struct
import os.path
import os
import settings as cfg

import shutil
import winsound
import random
logsWroteSoFar = []
FilesCopiedSoFar = []
randomLogFirstTime = True;
def getGameVersion():
    return cfg.config['intvars'].getint('CurrentGameVersion')
def PS3Version():
    if getGameVersion() == 1:
        return True
    else:
        return False
def offSetSeed(offset):
        random.seed(str(cfg.internalSeed)+str(offset))
def ErrorWindow(Message):
    winsound.MessageBeep()
    ctypes.windll.user32.FlashWindowEx(
    ctypes.windll.user32.MessageBoxW(None, Message,"Error", 0))

def GeneralMessageWindow(Message,Title):
    winsound.MessageBeep()
    ctypes.windll.user32.MessageBoxW(None, Message,Title, 0)

def clearLogsWroteSoFar():
    global logsWroteSoFar,FilesCopiedSoFar
    logsWroteSoFar = []
    FilesCopiedSoFar = []

def writeRandomizationLog(fileModified):
    """Write/Append the file modified / path"""
    global randomLogFirstTime
    if not PS3Version():
        if(fileModified not in logsWroteSoFar):
            randomLog = open("randomizationLog.txt", "a")
            # write file

            if (not randomLogFirstTime):
                randomLog.write('\n')
            else:
                randomLogFirstTime = False
            writeNewline(randomLog,fileModified)
            print("Wrote to " + fileModified)
            writeNewline(randomLog," ")
            writeNewline(randomLog,"y")
            writeNewline(randomLog," ")
            randomLog.write("y")
            randomLog.close()
            logsWroteSoFar.append(fileModified)
    else:
        if(fileModified not in logsWroteSoFar):
            randomLog = open("UsedLog.log", "a")
            # write file
            if (not randomLogFirstTime):
                randomLog.write('\n')
            else:
                randomLogFirstTime = False
            writeNewline(randomLog,fileModified)
            print("Wrote to " + fileModified)
            randomLog.write("y")
            randomLog.close()
            logsWroteSoFar.append(fileModified)
    
def writeNewline(file,variable):
    file.write(variable + "\n")
    
def unpackfromBinaryByte(bytes_var,typeOfChar = "i"):
    """ i == int (4 bytes)
        h = short (2 bytes)
        ? = bool (1 byte)
        depends on what we're reading
        """
    extraStr = "<"
    if getGameVersion() == 1: #PS3 Version
        extraStr=">"
    bytes_var = struct.unpack(extraStr+typeOfChar, bytes_var)
    bytes_var = bytes_var[0]
    return bytes_var

def readAndUnpack(file,amttoread):
    extraStr = ">"
    returnValue = file.read(amttoread)
    if(amttoread >= 4):
        returnValue = unpackfromBinaryByte(returnValue,"i")
    elif(amttoread >= 2):
        returnValue = unpackfromBinaryByte(returnValue,"h")
    elif(amttoread <= 1):
        returnValue = struct.unpack(extraStr+'H', b'\x00' + returnValue)[0]

    return returnValue
def readUnpackGoBack(file,amttoread):
    returnValue =readAndUnpack(file,amttoread)
    file.seek(-amttoread,1)
    return returnValue

def readHex(file,amttoread):
    returnValue = file.read(amttoread)
    returnValue = returnValue.hex()
    if(returnValue == ''):
        returnValue = 0
    else:
        returnValue = int(returnValue,16)
    
    return returnValue

def readHexPure(file,amttoread):
    """Read hex but zeros are BEGONE! """
    returnValue = file.read(amttoread)
    returnValue = returnValue.hex()
    returnValue = returnValue.strip('0')
    if(returnValue == ''):
        returnValue = 0
    else:
        returnValue = int(returnValue,16)
    return returnValue
def writeIntOrHex(file,amttoread,lenofBytes,forceEndian = ""):
    """ Convert to bytes"""
    extraStr = 'little'
    if getGameVersion() == 1:  # PS3 Version
        extraStr = 'big'
    if forceEndian != "":
        extraStr = forceEndian
    amttoread = amttoread.to_bytes(lenofBytes,byteorder=extraStr)
    returnValue = file.write(amttoread)
def writeFloat(file,amttoread,lenofBytes):
    """ Convert to bytes"""
    extraStr = "<"
    if getGameVersion() == 1:  # PS3 Version
        extraStr = ">"

    amttoread = struct.pack(extraStr+"f",amttoread)
    returnValue = file.write(amttoread)

def fileByteToHexToList(file,amttoread,split):
    """Grab byte into hex string then split into a list"""
    returnValue = file.read(amttoread)
    returnValue = returnValue.hex()
    returnValue = [returnValue[i:i+split] for i in range(0, len(returnValue), split)]
    return returnValue
def copyKHFile(filename):
    #returns true if specified file exists, return false if file is not in export dir
    exportString = 'export/KH2/'
    if PS3Version():
        exportString = 'export/'
    if (os.path.isfile(exportString + filename)):
        if filename not in FilesCopiedSoFar: #check if a file isnt there before copying otherwise we will overwrite any changes we've made in previous methods
            if not os.path.exists(os.path.dirname(filename)) and os.path.dirname(filename) != "":
                os.makedirs(os.path.dirname(filename))
            shutil.copyfile(exportString + filename, filename)
            print("Copying file...")
            FilesCopiedSoFar.append(filename)
            writeRandomizationLog(filename)
            return True
        else:
            return True
    else:
        return False





    