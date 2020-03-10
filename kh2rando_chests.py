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
    global ItemList
    ItemList = []
    ItemList = kh2rando_item.NewItemList()
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)() # retain local pointer to value
        return value                     # faster to return than dict lookup
def checkIfItemExists(list,itemCode):
    for x in list:
        if x.code == itemCode:
            return True
    return False
def findItemInList(list,itemCode):
    for x in list:
        if x.code == itemCode:
            return x

def CheckIfChestBlackListed(world,room,uid):
    room = int(room)
    if(world in kh2rando_itemTable.blackListUniqueID_Item):
        if(room in kh2rando_itemTable.blackListUniqueID_Item[world]):
            if(uid in kh2rando_itemTable.blackListUniqueID_Item[world][room]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def CheckIfChestMissable(world,room,uid):
    room = int(room)
    if(world in kh2rando_itemTable.missableItemListUniqueID_Item):
        if(room in kh2rando_itemTable.missableItemListUniqueID_Item[world]):
            if(uid in kh2rando_itemTable.missableItemListUniqueID_Item[world][room]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def randomizeAChest(Item,Type,WorldID,RoomIndex,UniqueChestID,EventID):
    """Notes:
        Spawn priority items first
        Dont spawn items marked with essential in optional content areas
        Dont spawn items marked with agrabah requirement in areas not accessible before agrabah 2
        
        agrabah requirement items cannot be in world : 01 03 04(COR), 07, 09,11(2ndvisit),12,0B
        optional requirement area blacklist : 09, 04(COR),0B

        COR ROOMS TO AVOID:
        15,16,17,18,19,1a
        We can also check what the original item was holding in the chest so we can see if it was optional or not.
        Only works for unique items though :(
        """
    def CheckInCavernOfRemembrance(WorldID,RoomID):
        CORRooms ={0x5,0x16,0x17,0x18,0x19,0x1a}
        if WorldID == 0x4 and RoomID in CORRooms:
            return True
        else:
            return False

    UniqueItemBlackList = {0x35,0x131,0x021A,0x1F1,0x219}
    PreGamePostGameBlacklistWlrds ={0x7,0x9,0x11,0x12,0xB} #Agrabah,100 Acre wood,Space paranoids,WTNW,Atlantica
    PostGameBlacklistWlrds ={0x9,0xB} #Poo's world,Atlantica
    NoEmptyItemsList = list(filter(lambda x: (x.emptyItem()),ItemList))


    if WorldID in PreGamePostGameBlacklistWlrds  or Item in UniqueItemBlackList or CheckInCavernOfRemembrance(WorldID,RoomIndex) or CheckIfChestMissable(WorldID,RoomIndex,UniqueChestID):
        NoEmptyItemsList = list(filter(lambda x: (not x.agrabahRequirement),NoEmptyItemsList))

    if WorldID in PostGameBlacklistWlrds or Item in UniqueItemBlackList or CheckInCavernOfRemembrance(WorldID,RoomIndex) or CheckIfChestMissable(WorldID,RoomIndex,UniqueChestID):
        NoEmptyItemsList = list(filter(lambda x: (not x.essential),NoEmptyItemsList))

    PriorityItemList = list(filter(lambda x: (x.priority),NoEmptyItemsList))
    CurrentList = PriorityItemList

    if(len(PriorityItemList) == 0 or CheckIfChestMissable(WorldID,RoomIndex,UniqueChestID)):
        CurrentList = list(filter(lambda x: (not x.priority),NoEmptyItemsList))

        
    #print(str(CurrentList) + "Before shuffiling")
    chosenItem = random.choice(CurrentList)
    fromNewList = ItemList.index(chosenItem)
    ItemList[fromNewList].subtractQOne()
    return ItemList[fromNewList].codeReturn()
        
    
        
def RandomizeChestContents(randomizeChests):
    offSetSeed(0)
    if (randomizeChests):
        print("Randomizing chests...")
        if (copyKHFile("03system.bin")):
            fileBin= open("03system.bin", "rb+")
            if (fileBin):
                TreasureFilePosition = 0
                TreasureFileSize = 0
                """So the way this works is that there is a value of hex inside 03system.bin that
                    has the fileposition of the treasure. we navigate to it and get the number of chests in the position in decimal.
                    hex editor displays hex backwards for some odd reason and makes reading pure hex annoying
                    
                    
                    more info:doing file.read(2) in binary files such as done below will be the equivalent of reading 0000
                    reading 1 for 00

                    """
                findHeaderinBAR(fileBin,'trsr',True)
                TreasureFilePosition = fileBin.tell()
                noChests = 0;
                UniqueChestID = 0 #We're going to make our own unique chest id cause I don't trust KH2 at all.
                fileBin.seek(2,1) #TrsrMagic
                noChests = readAndUnpack(fileBin,2) #noChests
                itemDict = Vividict()
                # because im dumb lets make a dictonary with unique chest item ids
                for i in range(noChests+1):
                    fileBin.seek(TreasureFilePosition + 4 + 2 + (i * 0xC), 0)
                    Item = readAndUnpack(fileBin,2) #Item ID that the chest currently contains.
                    Type = readHex(fileBin,1) #Type of item it is. 0 for chest, 1 for Event.
                    WorldID =  readHex(fileBin,1)#Which world is it? we can get that chest info here.
                    RoomIndex = readHex(fileBin,1) #Which room is it? we can get that chest info here.
                    RoomChestIndex = readHex(fileBin,1) #Which roomchestindex is it? we can get that chest info here.
                    EventID = readHex(fileBin,2)
                    itemDict[WorldID][RoomIndex][RoomChestIndex][Type][EventID][Item] = UniqueChestID
                    UniqueChestID +=1
                #because im dumb lets make a dictonary with unique chest item ids







                randomChestLoop = list(range(noChests+1))
                random.shuffle(randomChestLoop) #We will randomize the order we go through chests in in order to be a bit more random. Kinda odd but yea so we evenly spread out priority items instead of like in a row.
                for i in randomChestLoop:
                    Item = 0
                    Type = 0
                    fileBin.seek(TreasureFilePosition + 4 + 2 + (i * 0xC), 0)
                    Item = readAndUnpack(fileBin,2) #Item ID that the chest currently contains.
                    Type = readHex(fileBin,1) #Type of item it is. 0 for chest, 1 for Event.
                    WorldID =  readHex(fileBin,1)#Which world is it? we can get that chest info here.
                    RoomIndex = readHex(fileBin,1) #Which room is it? we can get that chest info here.
                    RoomChestIndex = readHex(fileBin,1) #Which roomchestindex is it? we can get that chest info here.
                    EventID = readHex(fileBin,2)
                    UniqueChestID = itemDict[WorldID][RoomIndex][RoomChestIndex][Type][EventID][Item]
                    fileBin.seek(TreasureFilePosition + 4 + 2 + (i * 0xC), 0) #reset back to original position for writing
                    """So now that we've gotten some info about the original item, we can do some randomization stuff
                    We can randomize a certain group of items depending on where the chest location is now that we have the world and room id of those locations."""
                    if (checkIfItemExists(ItemList,Item) and not CheckIfChestBlackListed(WorldID,RoomIndex,UniqueChestID)):
                        newChestVal = randomizeAChest(Item,Type,WorldID,RoomIndex,UniqueChestID,EventID)
                        writeIntOrHex(fileBin,newChestVal,2)


                        newitem = findItemInList(ItemList, newChestVal)
                        if isinstance(newitem,kh2rando_item.KHItem):
                            newItemName = newitem.name
                        else:
                            newItemName = "NoItemFound"

                        newitem = findItemInList(ItemList, Item)
                        if isinstance(newitem,kh2rando_item.KHItem):
                            oldItemName = newitem.name
                        else:
                            oldItemName = "NoItemFound"
                        writeOutCome_Chest(WorldID, RoomIndex,Type, UniqueChestID, oldItemName, newItemName)
                    
                fileBin.close()
            else:
                ErrorWindow("The file 03system.bin could not be opened. It's probably in use by another program or instance of this program.")
                
            writeRandomizationLog("03system.bin")
        else:
            ErrorWindow("03system.bin does not exist in the export/KH2/ folder. Make sure nothing has gone wrong during the extraction.")
    
