"""
Starting: Twilight Town
UNModifiablePath: Hollow Bastion 1
UNModifiablePath: Disney Castle
UNModifiablePath: Twilight Town revisit
ModifiablePaths:
Beast's Castle
Land of Dragons
Halloween Town
Agrabruh

revists:


Optional:
PrideLands
Atlantica

0a5c -- Unlock Mulan world and beast's world after HB
0ab8 -- TT revist
0acc -- Revisit HB?
0ae0 -- Visit Olympus Colsieum
0b34 -- complete port royal into Halloween town and agrabah
0b80 -- complete hwtown
0b94 -- complete agrabah
0ba8 -- recomplete mulan
0bb4 -- recomplete port royal
0be0 -- recomplete hwtown
0bec -- recomplete agrabah
0bf8 -- recomplete simba land
0c04 -- unlock gummi place mu
0c18 -- unlock gummi place bb
0c2c -- unlock gummi place olympus colsieum
0c58 -- unlock gummi place olympus colsieum
0c6c -- unlock gummi place olympus colsieum
0c80 -- unlock gummi place olympus colsieum
0cbc -- unlock gummi place olympus colsieum
0cd0 -- unlock gummi place olympus colsieum
0ce4 -- unlock gummi place olympus colsieum
0cf8 -- unlock gummi place olympus colsieum
0d0c -- unlock post game content -- simba land
0d48 -- unlock post game content -- alantica
0d5c -- unlock post game content -- simba land finisher
0d68 -- unlock gummi place  -- simba land finisher
0d7c --
-8a3c
7f40 wrldf
"""
from utils import writeRandomizationLog, readHex, readHexPure, readAndUnpack,readUnpackGoBack, fileByteToHexToList, writeIntOrHex,copyKHFile
from kh2rando_binUtils import findHeaderinBAR
#todo find how to trigger world progress if differing off the path otherwise it will reboot to title screen
def randomizeWorldRoutes():
    if shouldIRandomize:
        file = "00progress.bin"
        if (copyKHFile(file)):
            fileBin = open(file, "rb+")
            writeRandomizationLog(file)
            if (fileBin):
                findHeaderinBAR(fileBin, 'wldf', True)
                fileBin.seek(0x4,1) #skip a number
