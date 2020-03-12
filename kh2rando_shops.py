import os
import os.path
import random
import shutil
import kh2rando_item
import kh2rando_itemTable
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack,readUnpackGoBack, readHex, writeIntOrHex,copyKHFile,offSetSeed,PS3Version
from kh2rando_binUtils import findHeaderinBAR
from kh2rando_writeRandoOutcome import writeOutCome_ItemShop
def findItemInList(list,itemCode):
    for x in list:
        if x.code == itemCode:
            return x
def initVar():
    global ItemList_Shop
    ItemList_Shop = kh2rando_item.Generic_ItemList()
    for i in ItemList_Shop:
        if i.maximum != -1:
            i.maximum = 3 #max amount of times for an item to be in a shop
def randomizeShops(shouldIRandomize):
    offSetSeed(1)
    if shouldIRandomize:
        if (copyKHFile("03system.bin")):
            fileBin= open("03system.bin", "rb+")
            writeRandomizationLog("03system.bin")
            if (fileBin):
                def shopItemChanging():
                    findHeaderinBAR(fileBin,'shop',True)
                    itemsToChange = int(0x3a0/2) #Size divided by entry size to get total entries
                    fileBin.seek(0xC70,1) #skip all this data i dont know about and go to items
                    for shop_item in range(itemsToChange):
                        CurrentList = list(filter(lambda x: (x.emptyItem()), ItemList_Shop))
                        previousItem = readAndUnpack(fileBin,2)
                        fileBin.seek(-2, 1)
                        chooseShopItem = random.choice(CurrentList)
                        ItemList_Shop[ItemList_Shop.index(chooseShopItem)].subtractQOne()
                        writeIntOrHex(fileBin,chooseShopItem.codeReturn(),2)
                        writeOutCome_ItemShop(shop_item,"OLD: " + "{:<20}".format(findItemInList(ItemList_Shop,previousItem).name)+ "NEW:" + "{:<20}".format(chooseShopItem.name))

                def itemShopBuyingSellingPrices():
                    findHeaderinBAR(fileBin,'item',True)
                    fileBin.seek(0x4, 1)
                    itemsToChange = readAndUnpack(fileBin,4)
                    OrgPos = fileBin.tell()
                    for item in range(itemsToChange):
                        fileBin.seek(OrgPos + (item*0x18), 0)
                        itemID = readUnpackGoBack(fileBin,2)
                        fileBin.seek(0xC,1)
                        BuyPriceExisting = readUnpackGoBack(fileBin,2)
                        #loop through and find item in list
                        newItem = -1
                        for item_x in ItemList_Shop:
                            if item_x.codeReturn() == itemID:
                                newItem=item_x
                                break
                        if newItem != -1 and item_x.shopPrice != -1:
                            writeIntOrHex(fileBin,item_x.shopPrice,2) #Write new shop buy money
                            writeIntOrHex(fileBin,int(item_x.shopPrice*0.50),2) #Write new shop sell money times 0.50 of buy price
                if not PS3Version:
                    itemShopBuyingSellingPrices()
                    shopItemChanging()
            fileBin.close()

