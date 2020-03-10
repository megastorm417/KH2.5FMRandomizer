#Description Creates/Copies a mission file for boss enemies to use
import shutil
import os
import os.path
from utils import writeRandomizationLog, readHex, readHexPure, readAndUnpack,readUnpackGoBack, fileByteToHexToList, writeIntOrHex,copyKHFile,offSetSeed,PS3Version
from kh2rando_binUtils import findHeaderinBAR,findBarHeader,ModifyExtraFileNames,replaceAllStringInFile
regionFolders = {
    "fr",
    "gr",
    "it",
    "sp",
    "jp",
}
def msnFileCreate(fileName,curWorld,curRoom,oldMsnFileName): #pass in a mission file name, and the current room and world & will return the new Filename
    #lets check if the filename is equal to currentworld or currentroom
    #Lets also check if a mission file ID (last 3 digits) is already present in a room, otherwise we will overwrite something we wouldnt want to and have the player softlock
    oldMsnFileName = oldMsnFileName.rstrip(' \t\r\n\0')
    if (fileName[:4] == curWorld.upper() + curRoom.upper() ):
        return fileName #We dont need to do anything in this case.
    searchHeader = oldMsnFileName[:4]
    newFileName = curWorld.upper() + curRoom.upper() + fileName[4:] + '_R' #Add _R so we dont overwrite missions (_R == Randomized)
    importFolderName = "export/KH2/msn/jp/"
    if PS3Version():
        importFolderName = "export/msn/us/"
    exportFolderName = "msn/jp/"
    if PS3Version():
        exportFolderName = "msn/us/"
    if (os.path.isfile(importFolderName + fileName+ ".bar")):
        if not os.path.exists(exportFolderName):
            os.makedirs(exportFolderName)
        try:
            fileBin = open(importFolderName+oldMsnFileName.rstrip()+".bar",'rb+')
        except FileNotFoundError:
            fileBin = open(exportFolderName + oldMsnFileName + ".bar", 'rb+')
        barOffset = findBarHeader(fileBin)
        fileBin.seek(barOffset+0x18,0) #Skip to first header and get pos
        newPos = readAndUnpack(fileBin, 4)
        fileBin.seek(barOffset+newPos, 0)
        fileBin.seek(0xD, 1)
        oldBonusLevel = readAndUnpack(fileBin, 1)
        fileBin.close()
        shutil.copyfile(importFolderName + fileName+ ".bar", exportFolderName + newFileName + ".bar")
        print("Copying file...")
        writeRandomizationLog(exportFolderName + newFileName + ".bar")


        fileBin = open(exportFolderName + newFileName + ".bar",'rb+') #Modify file to use correct bonus level.
        ModifyExtraFileNames(fileBin,fileName,newFileName)
        #replaceAllStringInFile(fileBin,fileName.lower(),newFileName.lower())
        findHeaderinBAR(fileBin,fileName[:4],True)
        fileBin.seek(0xD,1)
        writeIntOrHex(fileBin,oldBonusLevel,1)
        fileBin.close()
        if PS3Version():
            for x in regionFolders:
                filestring = 'msn/' + x + "/" + newFileName + '.bar'
                if not os.path.exists('msn/' + x + '/'):
                    os.makedirs('msn/' + x + '/')
                shutil.copyfile(exportFolderName + newFileName + ".bar", filestring)
                print("Copying file for another region...")
                writeRandomizationLog(filestring)


        return newFileName
    else:
        print("Couldn't find msn file to copy...")
        return fileName
