import os
import os.path
import random
import shutil
import kh2rando_item
import kh2rando_itemTable
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack, readHex, writeIntOrHex,copyKHFile,offSetSeed
from kh2rando_writeRandoOutcome import writeOutCome_Chest
from kh2rando_binUtils import findHeaderinBAR

def initVar():
    global itemDropList
    itemDropList = kh2rando_item.Generic_ItemList()
def randomizeItemDrops(randomItemD,randomItemDP):
    offSetSeed(7)
    if (randomItemD or randomItemDP):
        print("Randomizing item drops from enemies...")
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", "rb+")
            if (fileBin):
                findHeaderinBAR(fileBin,'przt',True)
                fileBin.seek(4,1)

                #Size 0x18
                entryAmt = readAndUnpack(fileBin,4)
                entryPos = fileBin.tell()
                for x in range(entryAmt):
                    fileBin.seek(entryPos+(x*0x18),0)
                    entryIndex = readAndUnpack(fileBin,2)
                    droppedItemList = [0,0,0]
                    droppedItemListProbability = [0,0,0]
                    fileBin.seek(0xA,1)
                    writingPosition = fileBin.tell()
                    for i in range(3): #Clear it
                        writeIntOrHex(fileBin,0,2)
                        writeIntOrHex(fileBin,0,2)
                    #probability == percentage in clear num == 12% == 12 not 0.12 or anything silly
                    #Randomize items
                    if randomItemD:
                        for itemnum in range(len(droppedItemList)):
                            droppedItemList[itemnum] =random.choice(itemDropList).code
                    if randomItemDP:
                        for itemnum in range(len(droppedItemListProbability)):
                            chanceList = [random.randint(5,100),random.randint(5,50),random.randint(5,25)]
                            chanceList_Weight = [0.3,0.5,0.2]
                            newRando = random.choices(chanceList,k=1,weights=chanceList_Weight)[0]
                            droppedItemListProbability[itemnum] = newRando # 5% to 100 chance of an item dropping


                    #Write items
                    chanceList = [0,1,2,3]
                    randomItemAmount = random.choices(chanceList,k=1,weights=[0.7,0.3,0.2,0.1])[0]
                    """
                    fileBin.seek(entryPos + (x * 0x18), 0)
                    fileBin.seek(2,1)
                    orbSelectionList = []
                    orbListTypes = range(10)
                    for p in range(random.randint(0,3)): #Select types of the enemy will drop
                        orbSelectionList.append(random.choice(orbListTypes)) #Select which orb type to use
                    for e in range(0xA):
                        if e in orbSelectionList:
                            writeIntOrHex(fileBin,random.randint(0,5),1)#Write amount of orbs to drop
                        else:
                            fileBin.seek(1, 1)
"""
                    fileBin.seek(writingPosition,0)
                    for newRandomItems in range(randomItemAmount):
                        writeIntOrHex(fileBin,droppedItemList[newRandomItems],2)
                        writeIntOrHex(fileBin,droppedItemListProbability[newRandomItems],2)
            fileBin.close()

