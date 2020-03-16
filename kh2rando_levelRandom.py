from kh2rando_binUtils import openKHBinFile,findHeaderinBAR,findBarHeader
from kh2rando_ability import NewAbilityList
from kh2rando_abilityTable import Ability_Table
from utils import writeIntOrHex,readAndUnpack,copyKHFile,offSetSeed,PS3Version
import random
import math
import copy
import os
import os.path
from khenum import AbilityClass,AbilityTable_enum,KHCharacter,CharacterBoostType,AbilityType,AbilityTypeGained,FormTypeEnum
from kh2rando_writeRandoOutcome import writeOutCome_BonusLevel,writeOutCome_LevelUps
import kh2rando_itemTable
KHCharacterHPTable = {
    KHCharacter.Sora:0x05,
    KHCharacter.Donald:0x03,
    KHCharacter.Goofy:0x04,

}
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)() # retain local pointer to value
        return value                     # faster to return than dict lookup

def initVar():
    global AbilityList
    AbilityList = NewAbilityList()
def getAllFileNamesInFolder(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles
def RandomizeBonusLevels(bonusLevelBool,bonusItemBool,critBonusBool,extraAbilitiesInt,GiveGuard):
    offSetSeed(3)
    def getBonusLevelsFromMSN():
        fileBonuslevels = []
        path = "export/KH2/msn/jp/"
        if PS3Version():
            path = "export/msn/us/"
        msnFileList = getAllFileNamesInFolder(path)
        for msnFile in msnFileList:
            fileBin = open(path + msnFile, 'rb+')
            barOffset = findBarHeader(fileBin)
            fileBin.seek(0x18+barOffset, 0)  # Skip to first header and get pos
            newPos = readAndUnpack(fileBin, 4)
            fileBin.seek(newPos+barOffset, 0)
            fileBin.seek(0xD, 1)
            fileBonuslevels.append(readAndUnpack(fileBin, 1))
            fileBin.close()
        fileBonuslevels = sorted(list(dict.fromkeys(fileBonuslevels)))
        return fileBonuslevels


    if GiveGuard:
        newList = list(filter(lambda d: d.code == 0x052, AbilityList[AbilityTable_enum.Action]))  # Check for same character
        newList[0].maximum = 0
    if extraAbilitiesInt == 2: #If user asks for more abilities
        newList = list(filter(lambda d: d.character == KHCharacter.Sora,AbilityList[AbilityTable_enum.Support]))  # Check for same character
        newList = list(filter(lambda d: d.abilitytype == AbilityType.Additive, newList))
        #Grab from level up pool too!
        newList2 = list(filter(lambda d: d.character == KHCharacter.Sora,AbilityList[AbilityTable_enum.LevelUp]))  # Check for same character
        newList2 = list(filter(lambda d: d.abilitytype == AbilityType.Additive, newList2))
        newList  = newList+newList2
        for i in range(20): #Give like 20 more bonus abilities
            itemToCopy = random.choices(newList,k=1)[0]
            itemCopied = copy.deepcopy(itemToCopy)
            itemCopied.abilityLearned= AbilityTypeGained.Normal
            AbilityList[AbilityTable_enum.Support].append(itemCopied)

    if critBonusBool:
        # Randomize critical mode abilities by setting them to normal and grabbing random normal abilities
        newList = list(filter(lambda d: d.character == KHCharacter.Sora,
                              AbilityList[AbilityTable_enum.Support]))  # Check for same character
        newList = list(filter(lambda d: d.abilityLearned == AbilityTypeGained.CriticalBonus, newList))
        newList = list(filter(lambda d: d.emptyItem(), newList))
        critAbilitiesNum = 0
        for abilityitem in newList:
            critAbilitiesNum += abilityitem.maximum
            abilityitem.abilityLearned = AbilityTypeGained.Normal

        amountOfAbilitiesNum = 0
        while amountOfAbilitiesNum < critAbilitiesNum:
            newList = list(filter(lambda d: d.character == KHCharacter.Sora,AbilityList[AbilityTable_enum.Support]))
            newList = list(filter(lambda d: d.abilityLearned == AbilityTypeGained.Normal, newList))
            newList = list(filter(lambda d: d.emptyItem(), newList))

            itemsToBonus = random.choice(newList)
            index = AbilityList[AbilityTable_enum.Support].index(itemsToBonus)
            itemsToBonus = AbilityList[AbilityTable_enum.Support][index]
            if itemsToBonus.abilityLearned ==AbilityTypeGained.Normal:
                if itemsToBonus.maximum + amountOfAbilitiesNum <= critAbilitiesNum:
                    amountOfAbilitiesNum += itemsToBonus.maximum
                    itemsToBonus.abilityLearned = AbilityTypeGained.CriticalBonus
    #character,type of boost
    CharBoosts = []
    bonusLevelCharData= []
    for i in range(15):
        bonusLevelCharData.append([])
    abilityChoosing= []
    for i in range(15):
        abilityChoosing.append([])
    abilitesForEachChar= []
    for i in range(3):
        abilitesForEachChar.append(0)

    #get number of bonus abilities for each char
    for char in KHCharacter:
        amount = 0
        for type in range(len(AbilityList)):
            if type != AbilityTable_enum.LevelUp:
                for itemAb in AbilityList[type]:
                    if itemAb.character == char and itemAb.abilityLearned == AbilityTypeGained.Normal and itemAb.emptyItem():
                        amount +=1
        abilitesForEachChar[char] = amount



    for char in range(3):
        CharBoosts.append([0])
        for type in range(6):
            CharBoosts[char].append(0)
            #HP MP ARMOR ACCESSORY ITEM DRIVE
    maxCharBoosts = [[20,4,3,6,5,3],[18,0,1,0,2,1],[17,0,1,0,3,1]]
    def randomizeABonusLevel(hp, mp, armor, access, item, drive, abilityitem1, abilityitem2,char,bonslevel):
        nonlocal GiveGuard
        oldChar = char
        if char+1 == 0xE:  # If the character is roxas, change it to sora's num because theyre the same
            char = 0
        hp = mp = armor = drive = item = access = abilityitem2 = abilityitem1= 0 #Reset all
        currentNotifications = 0
        typeOfAbility = -1
        abilityitem1_name =""
        abilityitem2_name =""

        if bonslevel == 0x36:
            currentNotifications = 2 #Do not randomize Stats if the bonus level is 36/ Aerial recovery since it doesnt give that for some reason
            if GiveGuard:
                abilityitem1 = 0x052
                abilityitem1_name = "Guard (Forced)"
        if (BonusLevel not in bonusNumList):  # Blacklist bonus levels not in the game.
            currentNotifications = 2 #
        #handle ability swapping here


        if bonslevel in abilityChoosing[char]: #if the level we are is the same level that was randomly chosen to get an ability randomize by choosing between two ability types
            def filterListQuick(AbilityTp):
                newList = list(filter(lambda d: d.character == char, AbilityList[AbilityTp]))  # Check for same character
                newList = list(filter(lambda d: d.abilityLearned == AbilityTypeGained.Normal,newList))  # Normal abilities only
                newList = list(filter(lambda d: d.emptyItem(), newList))  # Check if empty ability
                return newList

            abilityChoosing[char].remove(bonslevel)
            possibleChoices = []
            for types in range(2):
                if  len(filterListQuick(types)) != 0:
                    possibleChoices.append(types)
            if len(possibleChoices) != 0:
                typeOfAbility = random.choice(possibleChoices)
                newList = filterListQuick(typeOfAbility)
                random.shuffle(newList)
                abilityitem1 = newList[0]
                index = AbilityList[typeOfAbility].index(abilityitem1)
                AbilityList[typeOfAbility][index].subtractQOne() #subtract cause we're using it
                abilityitem1 =AbilityList[typeOfAbility][index].code
                abilityitem1_name =AbilityList[typeOfAbility][index].name
                currentNotifications += 1

        usedThisRound = [0,0,0,0,0,0]
        while currentNotifications < 2: #Do stat boosts here
            randomizeBoostList = []

            for x in CharacterBoostType:
                if (CharBoosts[char][x] < maxCharBoosts[char][x] and not usedThisRound[x]):
                    randomizeBoostList.append(x)
            if len(randomizeBoostList) != 0:
                slotToRandomize = random.choices(randomizeBoostList,k=1)[0]


                #handle adding to new boosts
                for boosttype in CharacterBoostType:
                    if(slotToRandomize == boosttype):
                        if boosttype == CharacterBoostType.HPBoosts:
                            hp = KHCharacterHPTable[char]
                        if boosttype == CharacterBoostType.MPBoosts:
                            mp =0xa
                        if boosttype == CharacterBoostType.DriveUpgrades:
                            drive =1
                        if boosttype == CharacterBoostType.ArmorSlots:
                            armor =1
                        if boosttype == CharacterBoostType.Items:
                            item =1
                        if boosttype == CharacterBoostType.Accessory:
                            access =1
                        usedThisRound[boosttype] = True
                        CharBoosts[char][boosttype] += 1
                        currentNotifications += 1

            else:
                break
        if bonusItemBool and currentNotifications < 2:  # After everything is done and we still have an empty slot, give an bonus item
                tablesToChooseFrom = (kh2rando_itemTable.accessory_table,kh2rando_itemTable.synthesis_table,kh2rando_itemTable.item_table)
                weightTable = (0.5,0.4,0.8)
                choosenChoice = random.choices(tablesToChooseFrom,weights=weightTable,k=1)[0]
                choosenItemKey = random.choice(list(choosenChoice.keys()))
                choosenItem = choosenChoice[choosenItemKey]
                abilityitem2 = choosenItem[3]
                abilityitem2_name = choosenItemKey
                currentNotifications += 1
        if hp == 0 and mp == 0 and armor == 0 and drive == 0 and item == 0 and access == 0 and abilityitem1 == 0 and abilityitem2 == 0:
            alertDebug =0
        if (BonusLevel in bonusNumList):
            writeOutCome_BonusLevel(oldChar,bonslevel,
      "HP:" + "{:<4}".format(str(hp))
    + " MP:" + "{:<4}".format(str(mp))
    + " ARMOR:" + "{:<4}".format(str(armor))
    + " DRIVE:" + "{:<4}".format(str(drive))
    + " ITEM:" + "{:<4}".format(str(item))
    + " ACCESSORY:" + "{:<4}".format(str(access))
    + " Ability/Item:" + ("{:<20}".format(abilityitem1_name))
    + " Ability/Item 2:" + ("{:<20}".format(abilityitem2_name)))
        #Returning format might be wrong!!!!
        #hp mp drive?,item?,armor,access
        return (hp, mp,drive,item,armor,access,  abilityitem1, abilityitem2)





    if(bonusLevelBool):
        print("Modifying bonus levels...")
        bonusNumList = getBonusLevelsFromMSN()
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", 'rb+')  # skip like 4 hexs because it has useless data lol
            findHeaderinBAR(fileBin,'bons',True)
            if (fileBin):
                levelBonusStartPos = fileBin.tell() #gimmie our currentPosition
                fileBin.seek(4, 1)
                amtOfBonusLevels = readAndUnpack(fileBin, 4)  #
                for i in range(amtOfBonusLevels + 1): #Get the amount of bonus levels for specific characters
                    fileBin.seek(levelBonusStartPos + 8  + (i * 0x10), 0), # reset back to original position for writing thats coming up (Plus two to skip bonus level and character)
                    BonusLevel = readAndUnpack(fileBin, 1)  # Bonus level
                    Character = readAndUnpack(fileBin,1)  # Character value. 01 == sora 02 == donald 03 == goofy ...etc for others
                    if Character == 0xE:  # If the character is roxas, change it to sora's num because theyre the same
                        Character = 1
                    if (BonusLevel != 0x36 or not GiveGuard):
                        if (BonusLevel in bonusNumList): #Make sure the bonus level is actually used ingame.
                            bonusLevelCharData[Character-1].append(BonusLevel)
                #now that we have data, choose ability locations throughout the bonuses

                for char in KHCharacter:
                    for choicenum in range(abilitesForEachChar[char]):
                        newChoice = random.choice(bonusLevelCharData[char])
                        popout = bonusLevelCharData[char].pop(bonusLevelCharData[char].index(newChoice))
                        abilityChoosing[char].append(popout )



                randomBonusLevelLoop = list(range(amtOfBonusLevels + 1))
                random.shuffle(randomBonusLevelLoop)  # We will randomize the order we go through chests in in order to be a bit more random. Kinda odd but yea so we evenly spread out priority items instead of like in a row.

                for i in randomBonusLevelLoop:
                    fileBin.seek(levelBonusStartPos + 8  + (i * 0x10), 0), # reset back to original position for writing thats coming up (Plus two to skip bonus level and character)
                    BonusLevel = readAndUnpack(fileBin, 1)  # Bonus level
                    Character = readAndUnpack(fileBin,1)  # Character value. 01 == sora 02 == donald 03 == goofy ...etc for others
                    HPVal = readAndUnpack(fileBin, 1)  # HP Value.
                    MPVal = readAndUnpack(fileBin, 1)  # MP Value.
                    SlotUpgrades_Armor = readAndUnpack(fileBin, 1)  # Slot upgrade to player or party member
                    SlotUpgrades_Accessory = readAndUnpack(fileBin, 1)  # Slot upgrades to player or party member
                    SlotUpgrades_Item = readAndUnpack(fileBin, 1)  # Slot upgrades to player or party member
                    SlotUpgrades_Drive = readAndUnpack(fileBin, 1)  # Slot upgrades to player or party member
                    AbilityItem1 = readAndUnpack(fileBin, 2)  # Ability upgrades to player or party member
                    AbilityItem2 = readAndUnpack(fileBin, 2)  # Ability upgrades to player or party member
                    fileBin.seek(levelBonusStartPos + 8 + 2+ (i * 0x10), 0)
                    if(Character >= 1 and Character < 4 or Character == 0xE):
                        newbonusLevelVal = randomizeABonusLevel(HPVal, MPVal, SlotUpgrades_Armor,SlotUpgrades_Drive, SlotUpgrades_Item,SlotUpgrades_Accessory,  AbilityItem1, AbilityItem2,Character-1,BonusLevel)
                        for y in range(6):
                            writeIntOrHex(fileBin, newbonusLevelVal[y], 1) #write hp,mp,slot,slot,slot,slot
                        writeIntOrHex(fileBin, newbonusLevelVal[6], 2)  # write ability
                        writeIntOrHex(fileBin, newbonusLevelVal[7], 2)  # write ability


                fileBin.close()
def RandomizeDriveFormAbilities(shouldIrandomize):
    offSetSeed(4)
    if (shouldIrandomize):
        print("Modifying drive form abilities...")
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", 'rb+')  # skip 4 bytes
            findHeaderinBAR(fileBin, 'fmlv',True)  # skip 4 bytes
            if (fileBin):
                fileBin.seek(0x8, 1) #skip foward 8
                formData = []
                filePos = fileBin.tell()
                #Read
                for formType in FormTypeEnum:
                    formData.append([])
                    for formLevel in range(7):
                        formData[formType].append([])
                        fileBin.seek(0x2, 1)  # skip level byte, we know it already
                        AbilityFormLvlUp = readAndUnpack(fileBin, 2)
                        fileBin.seek(0x4, 1)
                        formData[formType][formLevel] = AbilityFormLvlUp
                #Modify
                formBonusNum = 200
                AutoAbility = {0x181, 0x183, 0x184}
                randomFormType = list(FormTypeEnum)
                random.shuffle(randomFormType)
                randomFormData = list(range(len(formData[formType])))
                random.shuffle(randomFormData)

                for formType in randomFormType:
                    for dt in randomFormData:
                        newList = list(filter(lambda d: d.character == KHCharacter.Sora, AbilityList[AbilityTable_enum.Support]))  # Check for same character
                        newList = list(filter(lambda d: d.abilityLearned == AbilityTypeGained.DriveForm,newList))
                        newList = list(filter(lambda d: d.emptyItem(), newList))  # Check if empty ability
                        random.shuffle(newList)
                        if formType in range(1,6):
                            if formData[formType][dt] != 0:
                                name = ""
                                if formData[formType][dt] == 0x181:
                                    name = 'Auto Valor'
                                if formData[formType][dt] == 0x183:
                                    name = 'Auto Master'
                                if formData[formType][dt] == 0x184:
                                    name = 'Auto Final'
                                if formData[formType][dt] not in AutoAbility:
                                    if len(newList) != 0:
                                        fromNewList = AbilityList[AbilityTable_enum.Support].index(newList[0])
                                        AbilityList[AbilityTable_enum.Support][fromNewList].subtractQOne()
                                        formData[formType][dt] = AbilityList[AbilityTable_enum.Support][fromNewList].code
                                        name = AbilityList[AbilityTable_enum.Support][fromNewList].name
                                    else:
                                        name ='None.'
                                        formData[formType][dt] = 0

                                writeOutCome_BonusLevel(KHCharacter.Sora, formBonusNum, str(formType.name) + ":" +name)
                        formBonusNum += 1

                #Write
                fileBin.seek(filePos,0)
                for formType in FormTypeEnum:
                    formData.append([])
                    for formLevel in range(7):
                        formData[formType].append([])
                        fileBin.seek(0x2, 1)  # skip level byte, we know it already
                        AbilityFormLvlUp = writeIntOrHex(fileBin,formData[formType][formLevel], 2)
                        fileBin.seek(0x4, 1)

            fileBin.close()


def RandomizeCriticalBonusAbilities(shouldIrandomize,shouldIrandomize2):
    offSetSeed(5)
    if (shouldIrandomize and shouldIrandomize2):
        print("Modifying critical bonus abilities...")
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", 'rb+')
            findHeaderinBAR(fileBin, 'plrp',True)  # skip to nearest bar closest to where we want to go
            if (fileBin):
                fileBin.seek(0x1f94, 1) #skip to critical mode abilities
                currentPos = fileBin.tell()
                critBonusNum = 300
                for i in range(7):
                    fileBin.seek(currentPos + (i*2),0)
                    OldAbility = readAndUnpack(fileBin,2)
                    fileBin.seek(-2, 1)  # Go bak
                    if OldAbility != 0x194: #Do not randomize no exp
                        newList = list(filter(lambda d: d.character == KHCharacter.Sora,AbilityList[AbilityTable_enum.Support]))  # Check for same character
                        newList = list(filter(lambda d: d.abilityLearned == AbilityTypeGained.CriticalBonus, newList))
                        newList = list(filter(lambda d: d.emptyItem(), newList))
                        if len(newList) != 0:
                            random.shuffle(newList)
                            fromNewList = AbilityList[AbilityTable_enum.Support].index(newList[0])
                            AbilityList[AbilityTable_enum.Support][fromNewList].subtractQOne()
                            writeIntOrHex(fileBin,AbilityList[AbilityTable_enum.Support][fromNewList].code,2)
                            writeOutCome_BonusLevel(KHCharacter.Sora, critBonusNum, AbilityList[AbilityTable_enum.Support][fromNewList].name)
                            critBonusNum+=1


def RandomizeLevelUps(shouldIrandomize):
    offSetSeed(6)
    if(shouldIrandomize):
        print("Modifying level ups for all characters...")
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", 'rb+') # skip like 4 hexs because it has useless data lol
            findHeaderinBAR(fileBin,'lvup',True)
            if (fileBin):
                levelUpsStartPos = fileBin.tell() #gimmie our currentPosition
                fileBin.seek(0x40, 1)
                amtOfLevels = readAndUnpack(fileBin, 4)
                #choose some abilities for some choices
                LVLLength = len(AbilityList[AbilityTable_enum.LevelUp])
                lvlAbilitiesList = [[],[],[]]
                for lvlupability in AbilityList[AbilityTable_enum.LevelUp]:
                    lvlAbilitiesList[0].append( (lvlupability.code,lvlupability.name) ) #Sword
                    lvlAbilitiesList[1].append( (lvlupability.code,lvlupability.name) ) #Shield
                    lvlAbilitiesList[2].append( (lvlupability.code,lvlupability.name) ) #Staff
                #now shuffle
                random.shuffle(lvlAbilitiesList[0])
                random.shuffle(lvlAbilitiesList[1])
                random.shuffle(lvlAbilitiesList[2])
                noneString = ''
                emptyTuple = (0,noneString)
                AbilityLevelsNums = random.choices(range(1,amtOfLevels),k=LVLLength) #I'd love to do indiviudal levels based on sword,shield  & staff but that would mean weaker lvls
                for chars in range(13):
                    stats = [random.randint(0,5),random.randint(0,5),random.randint(0,5),random.randint(0,5)]
                    if(chars==0): #sora
                        stats = [2,6,2,0]
                    if(chars==1): #donald
                        stats = [1,5,2,5]
                    if(chars==2): #goofy
                        stats = [5,0,2,4]
                    SwordAbility_Modified = emptyTuple
                    ShieldAbility_Modified = emptyTuple
                    StaffAbility_Modified = emptyTuple
                    for i in range(amtOfLevels):
                        beforeMoving = fileBin.tell()
                        CurrentLevel = i+1
                        writeOutCome_LevelUps(chars, i,
                                                " STR:" + "{:<4}".format(str(stats[0]))
                                              + " MAGIC:" + "{:<4}".format(str(stats[1]))
                                              + " DEF:" + "{:<4}".format(str(stats[2]))
                                              + " AP:" + "{:<4}".format(str(stats[3]))
                                              + " SwordAbility:" + "{:<20}".format(str(SwordAbility_Modified[1]))
                                              + " ShieldAbility:" + "{:<20}".format(str(ShieldAbility_Modified[1]))
                                              + " StaffAbility:" + "{:<20}".format(str(StaffAbility_Modified[1]))
                                              )
                        #EXPNeeded = readAndUnpack(fileBin,4)
                        fileBin.seek(8, 1) #skip exp and stats
                        if (chars == 0):
                            SwordAbility = readAndUnpack(fileBin, 2)
                            ShieldAbility = readAndUnpack(fileBin, 2)
                            StaffAbility = readAndUnpack(fileBin, 2)
                        else:
                            fileBin.seek(0x6, 1)
                        fileBin.seek(beforeMoving, 0) #go back to beginning
                        fileBin.seek(4, 1) #skip exp
                        writeIntOrHex(fileBin,stats[0],1) #write stats
                        writeIntOrHex(fileBin,stats[1],1)
                        writeIntOrHex(fileBin,stats[2],1)
                        writeIntOrHex(fileBin,stats[3],1)
                        if (chars == 0):
                            writeIntOrHex(fileBin,SwordAbility_Modified[0],2)
                            writeIntOrHex(fileBin,ShieldAbility_Modified[0],2)
                            writeIntOrHex(fileBin,StaffAbility_Modified[0],2)
                        else:
                            fileBin.seek(0x6,1)
                        #--Increase stats for next time--
                        #we can only increase 1 or 2 values depending on the ability that is present otherwise the game will not know how to handle it and crash
                        SwordAbility_Modified = emptyTuple
                        ShieldAbility_Modified = emptyTuple
                        StaffAbility_Modified = emptyTuple
                        if (i not in AbilityLevelsNums or chars != 0):
                            statsAmtToRandomize = 2
                        else:
                            #We will randomize the abilities now
                            SwordAbility_Modified = lvlAbilitiesList[0].pop(0)
                            ShieldAbility_Modified = lvlAbilitiesList[1].pop(0)
                            StaffAbility_Modified = lvlAbilitiesList[2].pop(0)
                            statsAmtToRandomize = 1

                        randomStat = [0,1,2,3]
                        endingList = []
                        for x in range(statsAmtToRandomize):
                            randomnum =random.randint(0,len(randomStat)-1)
                            poppednum = randomStat.pop(randomnum)
                            endingList.append(poppednum)
                        for y in endingList:
                            stats[y]+= random.randint(0,3)
                        #STR = readAndUnpack(fileBin,1)
                        #MAG = readAndUnpack(fileBin,1)
                        #DEF = readAndUnpack(fileBin,1)
                        #AP = readAndUnpack(fileBin,1)

                        fileBin.seek(2, 1)  # skip two bytes
                    fileBin.seek(0x4, 1)  # skip four bytes







            fileBin.close()
def ReduceFormGrinding(shouldIreduce):
    if (shouldIreduce):
        print("Reducing form grinding...")
        if (copyKHFile("00battle.bin")):
            fileBin = open("00battle.bin", 'rb+')  # skip 4 bytes
            findHeaderinBAR(fileBin, 'fmlv', True)  # skip 4 bytes
            if (fileBin):
                fileBin.seek(0x8, 1) #skip foward 8
                for formType in range(5):
                    for formLevel in range(6):
                        levelUpsStartPos = fileBin.tell()  # gimmie our currentPosition
                        fileBin.seek(0x1, 1)  # skip level byte, we know it already
                        FormLVL = readAndUnpack(fileBin, 1)
                        AbilityFormLvlUp = readAndUnpack(fileBin, 2)
                        FormLVLUpXP = readAndUnpack(fileBin, 4)
                        #times 0.40 drive xp
                        FormLVLUpXP = math.floor(FormLVLUpXP*0.37)
                        fileBin.seek(-4, 1)
                        writeIntOrHex(fileBin, FormLVLUpXP, 4)
                    fileBin.seek(0x8, 1)





            fileBin.close()