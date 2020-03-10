import os
import os.path
import random
import shutil
import kh2rando_item
import kh2rando_ability
import kh2rando_itemTable
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack, readHex, writeIntOrHex,copyKHFile,offSetSeed
from kh2rando_writeRandoOutcome import writeOutCome_Chest
from kh2rando_binUtils import findHeaderinBAR
from khenum import itemType,EquipmentStats,AbilityTable_enum,AbilityType,KHCharacter
def initVar():
    global newItemList,newAbilityList
    newItemList = kh2rando_item.NewItemList()
    newAbilityList = kh2rando_ability.NewAbilityList()
    newAbilityList = list(filter(lambda x: (x.abilitytype == AbilityType.Additive), newAbilityList[AbilityTable_enum.LevelUp]))
    newAbilityList.append( kh2rando_ability.KHSLAbility('Light and Darkness',KHCharacter.Sora,0x021D,abilitytype= AbilityType.Normal)) # Add light and darkness cause its not normally in the list
    newItemList = list(filter(lambda x: (x.type == itemType.Accessory or x.type == itemType.Armor or x.type == itemType.Equipment), newItemList)) #Filter to armor,accessory or equipment
    newItemList.append(kh2rando_item.KHItem('Ultima Weapon',code = 0x1F4,type =itemType.Equipment)) #Add ultima weapon
    newItemList.append(kh2rando_item.KHItem('Kingdom Key',code = 0x29,type =itemType.Equipment)) #add kingdom key

def randomizeEquipmentStats(randomEquipStat,randomEquipAbility):
    offSetSeed(8)
    if (randomEquipStat or randomEquipAbility):
        print("Randomizing equipment stats...")
        if (copyKHFile("03system.bin")):
            fileBin = open("03system.bin", "rb+")
            if (fileBin):
                findHeaderinBAR(fileBin,'item',True)


                #Size 0x18
                fileBin.seek(4, 1) #Skip ??
                entryAmt = readAndUnpack(fileBin,4)
                entryPos = fileBin.tell()
                StatusEffectIdList = []
                for x in range(entryAmt):
                    fileBin.seek(entryPos+(x*0x18),0)
                    ItemID = readAndUnpack(fileBin, 2)
                    CategoryID = readAndUnpack(fileBin, 1) #This is really conflicting. Sometimes the status ID is only 2 bytes away and sometimes its 4. :<
                    if CategoryID == 0x0E or CategoryID == 0x0F: #If armor or accessory
                        fileBin.seek(1,1)
                    elif CategoryID == 0x02 or CategoryID == 0x03 or CategoryID == 0x04 : #If keyblade/shield/staff
                        fileBin.seek(3,1)
                    else:
                        continue #Skip, we dont want any other item if it isnt an armor, accessory or keyblade/weapon
                    StatusID = readAndUnpack(fileBin, 2)
                    StatusEffectIdList.append((StatusID,ItemID))

                RealStatusItems = [] #if the item matches up with an equipment, accessory or armor item we will add it to the list along with its object for later reference
                for itemThing in StatusEffectIdList:
                    for itemReal in newItemList:
                        if itemReal.code == itemThing[1] and itemThing[0] != 0:
                            RealStatusItems.append((itemThing[0],itemReal))


                fileBin.seek(entryPos + (entryAmt * 0x18), 0)
                statusModifier = []
                for whatever in range(12):
                    statusModifier.append(0)
                fileBin.seek(4, 1)
                statusAmt = readAndUnpack(fileBin,4) #I counted
                statusPos = fileBin.tell()
                for x in range(statusAmt):
                    statusPos_Entry = fileBin.tell()
                    statsID = readAndUnpack(fileBin,2)
                    abilityID = readAndUnpack(fileBin,2)
                    for d in range(12):
                        statusModifier[d] = readAndUnpack(fileBin,1)

                    #Modify
                    ifinStatusItem = False
                    itemToUse = None
                    for xd in RealStatusItems:
                        if xd[0] == statsID:
                            itemToUse = xd[1]
                            ifinStatusItem = True
                            break

                    if ifinStatusItem:
                        fileBin.seek(statusPos_Entry+2,0)
                        if randomEquipAbility:
                            if itemToUse.type == itemType.Equipment or itemToUse.type == itemType.Accessory:
                                abilityID = random.choice(newAbilityList).code
                        if randomEquipStat:
                            if itemToUse.type == itemType.Equipment or itemToUse.type == itemType.Accessory:
                                statusModifier[EquipmentStats.StrengthStat] = random.randint(1,20)
                                statusModifier[EquipmentStats.MagicStat] = random.randint(1,20)
                            if itemToUse.type == itemType.Accessory:
                                statusModifier[EquipmentStats.APStat] = random.randint(1,30)
                            if itemToUse.type == itemType.Armor:
                                statusModifier[EquipmentStats.DefenseStat] = random.randint(1,10)
                                for resistNums in range(4,9):
                                    statusModifier[resistNums] = random.randint(75,150) #Not too OP, but gives the chance of reducing resistance
                                #for resistNums in range(9,10): #Global resist and invisible stuff so dont go too crazy
                                    #statusModifier[resistNums] = random.randint(80,120)
                        writeIntOrHex(fileBin,abilityID,2)
                        for d in range(12):
                            writeIntOrHex(fileBin,statusModifier[d],1)



