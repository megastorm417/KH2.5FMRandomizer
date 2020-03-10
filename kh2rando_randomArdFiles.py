import shutil
import os
import os.path
import struct
import random

from utils import writeRandomizationLog, readHex, readHexPure, readAndUnpack,readUnpackGoBack, fileByteToHexToList,writeFloat, writeIntOrHex,copyKHFile,offSetSeed,PS3Version,unpackfromBinaryByte
from kh2rando_binUtils import findHeaderinBAR,ReverseEndianString,findBarHeader
from kh2rando_writeRandoOutcome import writeOutCome_Enemy,writeOutCome_Boss,writeOutCome_SuperBoss,writeOutCome_Ally
from kh2rando_enemyTable import blackListUniqueID_Enemy,blackListGroup_Enemy,bossMSNTable,superBoss_table,boss_table,enemy_table,ally_table,blackListUCM_List,UCMProperties
from kh2rando_msnFile import msnFileCreate
from kh2rando_musicList import musicList,blackList_musicID

from kh2rando_ucmObject import NewEnemyList,NewBossList,NewSuperBossList,NewAllyList
from khenum import enemyMemoryUsage,enemyType
import math

class SpawnData:

    def __init__(self,noUCMSpawn=0,noLocationSpawn=0,noExtraData=0,noExtraData2=0,noExtraData3=0,positionInFile=0):
        self.noUCMSpawn = noUCMSpawn;
        self.noLocationSpawn = noLocationSpawn;
        self.noExtraData = noExtraData;
        self.noExtraData2 = noExtraData2;
        self.noExtraData3 = noExtraData3;
        self.positionInFile = positionInFile;

def getAllFileNamesInFolder(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return onlyfiles

def CheckIfEnemyTypeInTable(UCM,Table):
    for x in Table:
        if Table[x][1] == UCM:
            return True
    else:
        return False
def EnemyProperty(UCM,Type):
    for x in UCMProperties:
        if x.code == UCM and x.type == Type:
            return x
def EnemyPropertyExists(UCM,Type):
    for x in UCMProperties:
        if x.code == UCM and x.type == Type:
            return True
    return False


def CheckIfEnemyBlackListed(world,room,uid):
    room = int(room)
    if(world.upper() in blackListUniqueID_Enemy):
        if(room in blackListUniqueID_Enemy[world.upper()]):
            if(uid in blackListUniqueID_Enemy[world.upper()][room]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def CheckIfMusicBlackList(world,room,uid):
    room = int(room)
    if(world.upper() in blackList_musicID):
        if(room in blackList_musicID[world.upper()]):
            if(uid in blackList_musicID[world.upper()][room]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def CheckIfGroupBlackListed(world,room,group):
    room = int(room)
    if(world.upper() in blackListGroup_Enemy):
        if(room in blackListGroup_Enemy[world.upper()]):
            if(group in blackListGroup_Enemy[world.upper()][room]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def initVar():
    global EnemyList,BossList,SuperBossList,AllyList
    EnemyList = NewEnemyList()
    BossList = NewBossList()
    SuperBossList = NewSuperBossList()
    AllyList = NewAllyList()
def RandomizeARD(randomizeEnemies, randomizeBosses,randomizeAllies, KH2SoraForced,PS2EnemyOptimizations):
    def ucmPropertyModify(UCM,enemyType):
        fileBin.seek(position, 0)
        if EnemyPropertyExists(UCM,enemyType):
            ps3Offset = 0
            if PS3Version():
                ps3Offset = 2

            if EnemyProperty(UCM,enemyType).extraEnemyData != -1:
                fileBin.seek(0x20+ps3Offset, 1)  # Skip 20, find super boss variable
                writeIntOrHex(fileBin, EnemyProperty(UCM,enemyType).extraEnemyData, 2)
            else:
                fileBin.seek(0x20+ps3Offset, 1)  # Skip 20, find super boss variable
                writeIntOrHex(fileBin, 0, 2)
            if EnemyProperty(UCM,enemyType).extraEnemyData2 != -1:
                fileBin.seek(position, 0)
                fileBin.seek(0x24+ps3Offset, 1)  # Skip 20, find super boss variable
                writeIntOrHex(fileBin, EnemyProperty(UCM,enemyType).extraEnemyData2, 2)
            oldPos = [0,0,0] #Modify XYZ
            fileBin.seek(position, 0)
            for  i in range(len(oldPos)):
                oldPos[i] = unpackfromBinaryByte(fileBin.read(4),'f')
            for  i in range(len(oldPos)):
                oldPos[i] += EnemyProperty(UCM,enemyType).positionOffset[i]
            for  i in range(len(oldPos)):
                fileBin.seek(position + 4 + (i * 4), 0)
                writeFloat(fileBin, oldPos[i], 4)


        fileBin.seek(position, 0)
    def filterUcmProperty(List):
        for x in UCMProperties:
            if not x.useEnemyInRandomEnemyGen:
                List = list(filter(lambda d: (x.code != d.code), List))
        return List
    def replaceableUCMproperty(UCM,Type):
        if EnemyPropertyExists(UCM,Type):
            return EnemyProperty(UCM,Type).replaceEnemyInRandomization
        else:
            return True
    offSetSeed(2)
    filteredBossList = filterUcmProperty(BossList)
    bossListWeights = []
    randomLittleChests = [0x140,0x141,0x142,0x143,0x332,0x333,0x334,0x335,0x336,0x337,0x338,0x339,0x85e,0x8BB]
    randomBigChests = [0x144,0x145,0x33a,0x33b,0x33c,0x33d,0x33e,0x33f,0x340,0x341,0x342,0x343,0x343,0x08BC,0x9EC]

    for i in range(len(filteredBossList)):
        bossListWeights.append(random.uniform(0.7,1.0)) #random cause why the hell not



    def subSpawnChanging(var):
        nonlocal spawnData,fileBin,TotalSubSpawn
        if spawnData[var].noExtraData > 0 :
            noTransforms = 0
            fileBin.seek(TotalSubSpawn + 2,0)
            noTransforms = readAndUnpack(fileBin,2)
            TotalSubSpawn += 0x8 + (noTransforms* 0xC)
        if spawnData[var].noExtraData2 > 0 :
            TotalSubSpawn += (0x10 * spawnData[var].noExtraData2)
        if spawnData[var].noExtraData3 > 0 :
            TotalSubSpawn += (8 * spawnData[var].noExtraData3)


    print("Modifying enemies & bosses...")

    path = "export/KH2/ard"
    if PS3Version():
        path = "export/ard/us"
    fileList = getAllFileNamesInFolder(path)
    path2 = "export/KH2/msn/jp/"
    if PS3Version():
        path2 = "export/msn/jp/"
    msnFileList = getAllFileNamesInFolder(path2)
    if randomizeBosses:
        removeDMFromBosses()
    for j in fileList:
        EntryName = []
        EntryPositions = []
        EntrySizes = []
        filename = j
        currentWorld =filename[0:2]
        currentRoom  =filename[2:4]
        """Memory usage notes:
        Can't have too many unique enemies/ too many high memory usage enemies either
        All enemy data is loaded on room loadin and stored to prevent having to find a model file on every enemy spawn
        It explains why the game might crash sometimes on room loads, we run out of memory simply.
        We can check if a room's memory is low by loading in a help tutorial where images are simply not loaded because it costs too much.
        """

        #shutil.copyfile(path+ "/" +filename, "ard/"+filename) #Move to native folder
        regionExtraFolder = ""
        if PS3Version():
            regionExtraFolder = "us/"
        filename = "ard/"+regionExtraFolder+filename

        noEntries = 0

        if copyKHFile(filename):
            writeRandomizationLog(filename)
            fileBin = open(filename, 'rb+')
            barHeaderOffset=  findBarHeader(fileBin)
            fileBin.seek(barHeaderOffset+0x4,0)
            noEntries = readAndUnpack(fileBin,4);
            UniqueEnemyID = 0
            if noEntries > 0:
                for k in range(noEntries):
                    EntryName.append("")
                    EntryPositions.append(0)
                    EntrySizes.append(0)
                    fileBin.seek(barHeaderOffset+0x14 + (0x10 * k), 0)
                    buffer = fileBin.read(4)# read and then somehow change the last hex num into a 0!
                    EntryPositions[k] = barHeaderOffset + readAndUnpack(fileBin,4)
                    EntrySizes[k] = readAndUnpack(fileBin,4)
                    EntryName[k] = buffer;
                for l in range(noEntries):
                    check = EntryName[l].decode("utf-8")
                    check =ReverseEndianString(check, 1)
                    entrySize = EntrySizes[l]
                    starterNames = ["b_","m_","z_","p_","e_"]
                    if(check[0:2] in starterNames) and entrySize > 0 and filename[len(filename)-8:] not in {"al08.ard","po10.ard","eh23.ard"}:
                        noSubSpawns = 0
                        fileBin.seek(EntryPositions[l]+0x4,0)
                        noSubSpawns = readAndUnpack(fileBin,4)
                        
                        if noSubSpawns > 0:
                            spawnData = []
                            for x in range(noSubSpawns+1): #Create list in place of original codes vector and populate it with objects
                                spawnData.append(SpawnData())
                                
                            fileBin.seek(EntryPositions[l] + 0xC,0)
                            spawnData[0].noUCMSpawn = readAndUnpack(fileBin,2)
                            spawnData[0].noLocationSpawn = readAndUnpack(fileBin,2)
                            spawnData[0].noExtraData  = readAndUnpack(fileBin,2)
                            spawnData[0].noExtraData2 = readAndUnpack(fileBin,2)
                            spawnData[0].noExtraData3 = readAndUnpack(fileBin,2)
                                
                            TotalSubSpawn = EntryPositions[l] + 0x34 + ((spawnData[0].noUCMSpawn + spawnData[0].noLocationSpawn) * 0x40)
                            spawnData[0].positionInFile = EntryPositions[l] + 8
                                
                            subSpawnChanging(0)
                            #Get all spawn data.
                                
                            for c in range(1,noSubSpawns):
                                spawnData[c].positionInFile = TotalSubSpawn
                                fileBin.seek(TotalSubSpawn+4,0)
                                spawnData[c].noUCMSpawn = readAndUnpack(fileBin,2)
                                spawnData[c].noLocationSpawn = readAndUnpack(fileBin,2)
                                spawnData[c].noExtraData = readAndUnpack(fileBin,2)
                                spawnData[c].noExtraData2 = readAndUnpack(fileBin,2)
                                spawnData[c].noExtraData3 = readAndUnpack(fileBin,2)
                                    
                                TotalSubSpawn += 0x2C + ((spawnData[c].noUCMSpawn + spawnData[c].noLocationSpawn)* 0x40)  
                                subSpawnChanging(c)

                            randomizedUniqueEnemyList = []
                            randomizedUniqueEnemyListcodes = []
                            uniqueEnemyList = []
                            enemiesMaxWrittenUsage = [0, 0, 0]
                            enemiesUniqueMaxWrittenUsage = [0, 0, 0]
                            randomenemiesWrittenUsage = [0, 0, 0]
                            randomEnemiesUniqueWrittenUsage = [0, 0, 0]
                            if PS2EnemyOptimizations:
                                #Gathering data about the subspawns
                                for s in range(noSubSpawns):
                                    noUCMSpawns = spawnData[s].noUCMSpawn
                                    noSpawnObjects = spawnData[s].noLocationSpawn
                                    UCM = 0
                                    for b in range(noUCMSpawns):
                                        position = spawnData[s].positionInFile + 0x2C + (b * 0x40)
                                        fileBin.seek(position, 0)
                                        UCM = readAndUnpack(fileBin, 4)
                                        if CheckIfEnemyTypeInTable(UCM, enemy_table) and randomizeEnemies:
                                            # find weight of enemyenemiesMaxWrittenUsage
                                            memUsageFound = list(filter(lambda x: (x.code == UCM), EnemyList))[
                                                0].memoryUsage
                                            enemiesMaxWrittenUsage[memUsageFound] += 1
                                            if UCM not in uniqueEnemyList:
                                                enemiesUniqueMaxWrittenUsage[memUsageFound] += 1
                                                uniqueEnemyList.append(UCM)
                            # Modifiying the spawns
                            for s in range(noSubSpawns):
                                noUCMSpawns = spawnData[s].noUCMSpawn
                                noSpawnObjects = spawnData[s].noLocationSpawn
                                UCM = 0
                                for b in range(noUCMSpawns):
                                    position = spawnData[s].positionInFile + 0x2C + (b * 0x40)
                                        
                                    #EntryLimit = (EntryPositions[l] + EntrySizes[l])
                                    #if(position > EntryLimit)
                                    fileBin.seek(position,0)
                                    ps3Offset = 0
                                    if PS3Version():
                                        ps3Offset = 2
                                    UCM = readUnpackGoBack(fileBin,4)
                                    fileBin.seek(0x20+ps3Offset,1) #Skip 20, find if its a super boss version of a regular boss or not.
                                    DataBoss = readUnpackGoBack(fileBin,2)
                                    fileBin.seek(0x4, 1)  # Skip 20, find super boss variable
                                    DataBoss2 = readUnpackGoBack(fileBin, 2)
                                    #avoidUCMList = [0x237,0x238,0x319,0x31A,0x3EE] this is obsolete.
                                    if(not CheckIfEnemyBlackListed(currentWorld,currentRoom,UniqueEnemyID) and not CheckIfGroupBlackListed(currentWorld,currentRoom,check) ):
                                        fileBin.seek(position,0)  
                                        randomValue = 0

                                        def enemyBTLMSNEdit():
                                            #PS3 Version Note: Little Endian to Big Endian change: every 2 bytes is swapped. GREAT.
                                            #Bytearray=  "BB"[::-1] + "50"[::-1] + "M_"[::-1] + "1S"[::-1] + "40"[::-1] +".B"[::-1]
                                            """
                                            def replaceAllMSN(): #very destructive, has problems with ard files that has multiple bosses
                                                nonlocal x
                                                # write new mission file
                                                BeforeReplaced = fileBin.read(18)  # i assume 18 is the most?????
                                                fileBin.seek(0, 0)

                                                replace1 = BeforeReplaced.decode('utf-8').rstrip('\x00')
                                                strLength = len(bossMSNTable[x])
                                                strLength2 = len(replace1)
                                                spacingNum = strLength2 - strLength
                                                beforeEncode = bossMSNTable[x]
                                                beforeEncode = msnFileCreate(beforeEncode, currentWorld, currentRoom)

                                                for x in range(spacingNum):
                                                    beforeEncode += '\x00'
                                                for x in range(-spacingNum):
                                                    replace1 += '\x00'

                                                replace2 = str.encode(beforeEncode)
                                                replace1 = str.encode(replace1)
                                                # note: we should add extra bytes based on length so we dont offset the file if we replace stuff
                                                allData = fileBin.read()
                                                allData = allData.replace(replace1, replace2)  # oh my god i forget to store it back and i was wondering why it wasnt working
                                                fileBin.seek(0, 0)
                                                fileBin.write(allData)
                                            """
                                            def replaceOneMSN(newMSN):
                                                # write new mission file
                                                BeforeReplaced = fileBin.read(0x20)  # i assume 18 is the most?????
                                                BeforeReplaced = BeforeReplaced.decode('utf-8').rstrip('\x00')
                                                BeforeReplaced = ReverseEndianString(BeforeReplaced,2,True)
                                                fileBin.seek(-0x20, 1)

                                                beforeEncode = newMSN
                                                beforeEncode = msnFileCreate(beforeEncode,currentWorld,currentRoom,BeforeReplaced)
                                                beforeEncode = ReverseEndianString(beforeEncode, 2, True,True)
                                                spacingNum = 0x20 - len(beforeEncode)
                                                # note: we should add extra bytes based on length so we dont offset the file if we replace stuff
                                                for x in range(spacingNum):
                                                    beforeEncode += '\x00'

                                                replace2 = str.encode(beforeEncode)
                                                fileBin.write(replace2)
                                                fileBin.seek(-len(replace2), 1) #Write, go back and we're done.


                                            #end of utility functions. start of main function
                                            #This maybe need to be looked at again.
                                            btl_String = 'btl'
                                            findHeaderinBAR(fileBin,btl_String,True)
                                            # find "btl" header thing
                                            # go to position from the btl header
                                            endcodedCheck = ReverseEndianString(check,2,True).encode('utf-8')  # get entry name ex: b_00
                                            posBeforeRead = fileBin.tell()
                                            data2 = fileBin.read()

                                            seekToRead = data2.find(endcodedCheck)
                                            fileBin.seek(posBeforeRead, 0)
                                            fileBin.seek(seekToRead, 1)
                                            # goto name closest
                                            # find original msn by backing up a lil so we find the currentworld string
                                            posBeforeRead = fileBin.tell()
                                            seekToRead = -1
                                            offset = 0
                                            #15 00 09 find this byte and offset foward by 4 bytes and write this way
                                            while seekToRead != 0:  # This is slow..... But the best I can do ATM.
                                                fileBin.seek(posBeforeRead, 0)
                                                offset += 1
                                                if offset > 300:
                                                    return #We probrably can't find anything because an boss has already taken its place. In this case, we will just stop the function
                                                fileBin.seek(fileBin.tell() - offset, 0)
                                                data3 = fileBin.read()
                                                findThing =data3.find(b'\x15\x00\x09')
                                                if findThing == 0:
                                                    seekToRead = findThing+3+4 #Skip the byte we found and the following 4 bytes to get to the string
                                                    break;
                                            fileBin.seek(seekToRead, 1)
                                            fileBin.seek(posBeforeRead, 0)
                                            fileBin.seek(-offset, 1)
                                            offset = 0
                                            if not PS3Version():
                                                offset = 1
                                            fileBin.seek(seekToRead+offset, 1)
                                            testRead = fileBin.read(0x20)
                                            fileBin.seek(-0x20, 1)
                                            if ReverseEndianString(testRead.decode('utf-8'),2,True).rstrip('\x00') == "HB38_FM_MAR":
                                                replaceOneMSN("HB33_FM_LAR")
                                                enemyBTLMSNEdit()  # Try again......
                                            else:
                                                for x in bossMSNTable:
                                                    if enemyToWrite.code == x:
                                                        replaceOneMSN(bossMSNTable[x])


                                        if CheckIfEnemyTypeInTable(UCM, boss_table) and ( DataBoss2 != 1) and randomizeBosses and replaceableUCMproperty(UCM,enemyType.Boss):
                                            type = enemyType.Boss
                                            # get Random boss UCM value here!
                                            enemyToWrite = random.choices(filteredBossList, bossListWeights)
                                            enemyToWrite = enemyToWrite[0]
                                            if UCM != enemyToWrite.code:
                                                index = filteredBossList.index(enemyToWrite)
                                                bossListWeights[index] *= 0.56  # Decrease weight of object we just spawned for lesser chance of being picked next time
                                                writeIntOrHex(fileBin, enemyToWrite.code, 4)
                                                fileBin.seek(position, 0)
                                                ucmPropertyModify(enemyToWrite.code,type)

                                            writeOutCome_Boss(currentWorld, int(currentRoom), UniqueEnemyID, UCM, enemyToWrite.name, check)
                                            enemyBTLMSNEdit()
                                        elif CheckIfEnemyTypeInTable(UCM, enemy_table) and randomizeEnemies and replaceableUCMproperty(UCM,enemyType.Normal):
                                            type = enemyType.Normal
                                            # Get random Enemy UCM value here!
                                            # Choose 3 enemies to put in list as backup
                                            curEnemyList= filterUcmProperty(EnemyList)
                                            currentEnemyList = curEnemyList
                                            if PS2EnemyOptimizations:
                                                currentEnemyList = curEnemyList
                                                for maxwritten in range(len(enemiesUniqueMaxWrittenUsage)):  # Filter out if reached maximum enemies allowed
                                                    if randomEnemiesUniqueWrittenUsage[maxwritten] == enemiesUniqueMaxWrittenUsage[maxwritten]:
                                                        currentEnemyList = list(filter(lambda x: (x.memoryUsage != maxwritten), currentEnemyList))
                                                currentEnemyList = currentEnemyList + randomizedUniqueEnemyList

                                                # memUsageFound = list(filter(lambda x: (x.code == UCM), EnemyList))[0].memoryUsage
                                                # currentEnemyList = list(filter(lambda x: (x.memoryUsage == memUsageFound),currentEnemyList))
                                                for maxwritten in range(len(enemiesMaxWrittenUsage)):  # Filter out if reached maximum enemies allowed
                                                    if randomenemiesWrittenUsage[maxwritten] == enemiesMaxWrittenUsage[maxwritten]:
                                                        currentEnemyList = list(filter(lambda x: (x.memoryUsage != maxwritten), currentEnemyList))

                                            random.shuffle(currentEnemyList)
                                            enemyToWrite = currentEnemyList[0]
                                            randomenemiesWrittenUsage[enemyToWrite.memoryUsage] += 1
                                            ucmPropertyModify(enemyToWrite.code, type)
                                            writeIntOrHex(fileBin, enemyToWrite.code, 4)
                                            writeOutCome_Enemy(currentWorld, int(currentRoom), UniqueEnemyID, UCM,
                                                               enemyToWrite.name, check)
                                            if enemyToWrite.code not in randomizedUniqueEnemyListcodes:
                                                randomEnemiesUniqueWrittenUsage[enemyToWrite.memoryUsage] += 1
                                                randomizedUniqueEnemyList.append(enemyToWrite)
                                                randomizedUniqueEnemyListcodes.append(enemyToWrite.code)



                                        elif CheckIfEnemyTypeInTable(UCM, superBoss_table) and randomizeBosses and replaceableUCMproperty(UCM,enemyType.SuperBoss):
                                            type = enemyType.SuperBoss
                                            curEnemyList = filterUcmProperty(SuperBossList)
                                            # if not (currentWorld.upper() == "HB" and currentRoom == "33" and UCM == 0x933): #SOMEONE put vexen data into a place where he isnt suppost to be

                                            random.shuffle(curEnemyList)
                                            enemyToWrite = curEnemyList.pop(0)
                                            if UCM != enemyToWrite.code:
                                                writeIntOrHex(fileBin, enemyToWrite.code, 4)
                                                fileBin.seek(position, 0)
                                                ucmPropertyModify(enemyToWrite.code,type)
                                            writeOutCome_SuperBoss(currentWorld, int(currentRoom), UniqueEnemyID, UCM, enemyToWrite.name, check)
                                            enemyBTLMSNEdit()
                                        elif CheckIfEnemyTypeInTable(UCM, ally_table) and randomizeBosses and replaceableUCMproperty(UCM,enemyType.Ally):
                                            type = enemyType.Ally
                                            curEnemyList = filterUcmProperty(AllyList)
                                            # if not (currentWorld.upper() == "HB" and currentRoom == "33" and UCM == 0x933): #SOMEONE put vexen data into a place where he isnt suppost to be

                                            random.shuffle(curEnemyList)
                                            enemyToWrite = curEnemyList[0]
                                            ucmPropertyModify(enemyToWrite.code, type)
                                            writeIntOrHex(fileBin, enemyToWrite.code, 4)
                                            writeOutCome_Ally(currentWorld, int(currentRoom), UniqueEnemyID, UCM, enemyToWrite.code, check)
                                        elif UCM == 0x5AB and KH2SoraForced:
                                            # replace roxas skateboards with sora
                                            writeIntOrHex(fileBin, 0x81A, 4)
                                        elif UCM == 0x236 and currentWorld.upper() == "TT" and currentRoom == "34" and KH2SoraForced:
                                            # replace Sora with roxas for this fight
                                            writeIntOrHex(fileBin, 0x5A, 4)
                                        elif UCM == 0x236 and check == "b_42" and currentWorld.upper() == "TT" and currentRoom == "10" and KH2SoraForced:
                                            # replace Sora with roxas for this event
                                            writeIntOrHex(fileBin, 0x5A, 4)
                                        elif UCM == 0x236 and check == "b_40" and currentWorld.upper() == "TT" and currentRoom == "12" and KH2SoraForced:
                                            # replace Sora with roxas for this event
                                            writeIntOrHex(fileBin, 0x5A, 4)
                                        elif UCM in randomLittleChests:
                                            # replace Sora with roxas for this event
                                            writeIntOrHex(fileBin, random.choice(randomLittleChests), 4)
                                        elif UCM in randomBigChests:
                                            # replace Sora with roxas for this event
                                            writeIntOrHex(fileBin, random.choice(randomBigChests), 4)
                                        elif UCM == 0x988:
                                            # todo randomize puzzle pieces
                                            pass
                                        elif UCM in blackListUCM_List:
                                            writeIntOrHex(fileBin, 0, 4)  # Write nothing.


                                    UniqueEnemyID+=1
            #End of noentries if statement
            fileBin.close()
def randomizeMusic(ranMusic):
    if ranMusic:
        offSetSeed(50)
        print("Modifying music...")
        path = "export/KH2/ard"
        if PS3Version():
            path = "export/ard/us"
        fileList = getAllFileNamesInFolder(path)
        for j in fileList:
            musicOccurenceNum = 0
            musicListUsed= []
            filename = j
            currentWorld = filename[0:2].upper()
            currentRoom = int(filename[2:4])
            # shutil.copyfile(path+ "/" +filename, "ard/"+filename) #Move to native folder
            regionExtraFolder = ""
            if PS3Version():
                regionExtraFolder = "us/"
            filename = "ard/"+regionExtraFolder + filename
            if copyKHFile(filename):
                writeRandomizationLog(filename)
                fileBin = open(filename, 'rb+')
                """
                        Notes:
                        Affecting music data also affects the space of ram. Great. Some places may softlock because of this.....
                        Another music weighting system based on file size?
                        
                        EVT Data: Amt of entries not given. Size of entries not given. 
                        Anything after the evt bar entry in the main header will be in evt, btl header sometimes 
                        Start of EVT entry depending on event type:
                        Event ID, Used by a general event. EX: Bosses with their respective cutscene on death/enter
                        Empty?
                        Event 2ndID, Possibly a type? Changes and isnt very consistent.

                        Event 2ndID's when a boss is assigned to an eventId may be:
                        2C if 48 (Super Boss?)
                        22 if 44 (Normal Boss?)
                        possibly use an if statement if an value is above an amount
                        Music event starts with 10 00 01? Wow, what a waste of time trying to decipher this
                        5 Unknown Bytes,
                        Music Num Data, 0C == Current World music? 09 == Current World Battle Music?
                        Empty,
                        Music Num Data,

                        FF Sometimes ends the data, sometimes it doesn't.
                """
                if findHeaderinBAR(fileBin, 'evt', False):
                    fileBin.seek(0x8, 1)
                    evtSize = readAndUnpack(fileBin, 4)
                    """ Useless
                    eventIDList = []
                    if findHeaderinBAR(fileBin, 'map', False):
                        fileBin.seek(0x8, 1)
                        mapSize = readAndUnpack(fileBin, 4)
                        findHeaderinBAR(fileBin, 'map', True)  # go back and start going through
                        filePosition = fileBin.tell()
                        mapFileText = fileBin.read(mapSize)
                        fileBin.seek(filePosition, 0)
                        difBytes = [b'\x01\x00\x02']
                        for differentEvtTypes in difBytes:
                            curPos = 0
                            while (mapFileText.count(differentEvtTypes, curPos) != 0):
                                curPos = mapFileText.find(differentEvtTypes, curPos)  # Skip 5 bytes
                                fileBin.seek(filePosition + curPos, 0)
                                fileBin.seek(-0x4, 1)  # Go back, find 2nd id
                                eventIDList.append(readUnpackGoBack(fileBin, 1))
                                curPos += 1
                        if len(eventIDList) != 0:
                            debughi = 0
                    """
                    findHeaderinBAR(fileBin, 'evt', True)  # go back and start going through
                    filePosition = fileBin.tell()
                    evtFileText = fileBin.read(evtSize)
                    fileBin.seek(filePosition, 0)

                    difBytes = [b'\x10\x00\x01']

                    for differentEvtTypes in difBytes:
                        curPos = 0
                        while (evtFileText.count(differentEvtTypes, curPos) != 0):
                            curPos = evtFileText.find(differentEvtTypes, curPos)  # Skip 5 bytes
                            fileBin.seek(filePosition + curPos, 0)
                            if not CheckIfMusicBlackList(currentWorld,currentRoom,musicOccurenceNum):
                                fileBin.seek(-0x4, 1)  # Go back, find 2nd id
                                evtFirstEventID = readAndUnpack(fileBin, 1)
                                fileBin.seek(1, 1)
                                evtSecondEventID = readAndUnpack(fileBin, 1)
                                fileBin.seek(1, 1)
                                fileBin.seek(len(differentEvtTypes), 1)  # skip over what we just found
                                fileBin.seek(0x1, 1)  # skip empty
                                firstMusicID = readUnpackGoBack(fileBin, 1)
                                random.shuffle(musicList)
                                chooseNewMusic = musicList[0]
                                for xd in musicListUsed:
                                    if evtFirstEventID == xd[0]:
                                        chooseNewMusic =xd[1]
                                writeIntOrHex(fileBin, chooseNewMusic, 1)
                                fileBin.seek(0x1, 1)  # skip empty
                                firstMusicID2 = readUnpackGoBack(fileBin, 1)
                                writeIntOrHex(fileBin, chooseNewMusic, 1)
                                usedOnce = False
                                for xd in musicListUsed:
                                    if evtFirstEventID == xd[0]:
                                        usedOnce = True
                                if not usedOnce:
                                    musicListUsed.append((evtFirstEventID,chooseNewMusic))
                            curPos += 1
                            musicOccurenceNum+=1
                fileBin.close()


def removeEnemySpawnLimit(EnemiesWereRandomized):
    if EnemiesWereRandomized:
        enemyWeightValue = 0x8
        curFile = "00objentry.bin"
        if copyKHFile(curFile):
            writeRandomizationLog(curFile)
            fileBin = open(curFile, 'rb+')

            fileSize = os.path.getsize(curFile) #Get size since bin doesnt have an amount of objects
            offset = 0
            if PS3Version():
                fileSize-= 0x10
                offset = 0x10

            amtOfObjects = int(math.floor(fileSize/0x60))

            for objectEntry in range(amtOfObjects):
                fileBin.seek((objectEntry*0x60)+offset,0)
                fileBin.seek(0x8,1) #Skip to UCM code
                UCM = readAndUnpack(fileBin,4)
                fileBin.seek(0x4, 1) #Skip unknown Data
                Object_STR = (fileBin.read(0x20)).decode("utf-8") #PS3 Version Name endian order was left unchanged.
                ObjectMSET_STR = (fileBin.read(0x20)).decode("utf-8")
                fileBin.seek(0xC, 1)  # Skip to spawn limit value
                if CheckIfEnemyTypeInTable(UCM,enemy_table) and Object_STR[:2] == "M_":
                    writeIntOrHex(fileBin,enemyWeightValue,1) #Write lower spawn limit value!
                if CheckIfEnemyTypeInTable(UCM,boss_table) or CheckIfEnemyTypeInTable(UCM,superBoss_table) and Object_STR[:2] == "B_":
                    writeIntOrHex(fileBin,enemyWeightValue,1) #Write lower spawn limit value!
                if CheckIfEnemyTypeInTable(UCM,ally_table) and Object_STR[:2] == "N_":
                    writeIntOrHex(fileBin,enemyWeightValue,1) #Write lower spawn limit value!
def removeDMFromBosses():
    #here we will remove ai functions from bosses that are problematic.
    removeAIFunction('obj/B_EX170.mdlx','rc_invitation_to_dark') #Remove xemnas skyscraper rc battle thing
    removeAIFunction('obj/B_EX170.mdlx','warp_building_front')
    removeAIFunction('obj/B_EX170_LV99.mdlx','rc_invitation_to_dark') #Do it for data xemnas

    removeAIFunction('obj/B_EX140.mdlx','change_space_battle') #Get rid of Xigbar room changing aspects
    removeAIFunction('obj/B_EX140.mdlx','change_space') #Get rid of Xigbar room changing aspects

    removeAIFunction('obj/P_BB000_BTL.mdlx','‰rc_heart_drive_movement') #Beast reaction command thing where he knocks out
    removeAIFunction('obj/P_BB000_BTL.mdlx','rc_heart_beat_stop')
    removeAIFunction('obj/P_BB000_BTL.mdlx','rc_heart_beat')
    removeAIFunction('obj/P_BB000_BTL.mdlx','rc_heart_drive_charge_stop')
    removeAIFunction('obj/P_BB000_BTL.mdlx','rc_heart_drive_charge')
    removeAIFunction('obj/P_BB000_BTL.mdlx','rc_heart_drive_movement_stop')
    if PS3Version():
        removeAIFunction('obj/B_BB110.mdlx','‰sora_downshock!') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','sora_spin!') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','spin_hit') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','chandelier_camera?') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','rc_step_jump') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','hop') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','reaction') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','spin_hit_start') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','revenge_catch_wait') #Dark Thorn Boss
        removeAIFunction('obj/B_BB110.mdlx','battle_catch_wait') #Dark Thorn Boss



        removeAIFunction('obj/N_HB630.mdlx','battle_start') #Sephiroth RC first attack crash
        removeAIFunction('obj/N_HB630.mdlx','rc_success') #Sephiroth RC first attack crash
        removeAIFunction('obj/N_HB630.mdlx','atk_split_flash') #Sephiroth RC first attack crash
def removeAIFunction(file,string):
    #Same for PS3 Version.
    if copyKHFile(file):
        fileBin = open(file, 'rb+')
        string = b'\x00' + string.encode('utf-8') + b'\x00'
        entireFile = fileBin.read()
        if string in entireFile:
            replaceString = len(string) * b'\x00'
            entireFile = entireFile.replace(string,replaceString)
            fileBin.seek(0,0)
            fileBin.write(entireFile)
            fileBin.close()
        else:
            fileBin.close()
        #Size: 0x60 file
        #Two strings, both total size of 0x20 Bytes
        #Get Spawnlimiter Value
        #Modify object entry if string starts with M_