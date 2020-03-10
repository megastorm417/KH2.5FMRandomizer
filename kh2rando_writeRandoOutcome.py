from kh2rando_enemyTable import superBoss_table,boss_table,enemy_table,ally_table
import os.path
import os
import version
import settings
worldsToText = {
'ES' : 'End of Sea',
'TT' : 'Twilight Town',
'DI' : 'Destiny Island',
'HB' : 'Hollow Bastion',
'BB' : 'Beast’s Castle',
'HE' : 'Olympus Coliseum',
'AL' : 'Agrabah',
'MU' : 'The Land of Dragons',
'PO' : '100 Acre Wood',
'LK' : 'Pride Land',
'LM' : 'Atlantica',
'DC' : 'Disney Castle',
'WI' : 'Timeless River',
'NM' : 'Halloween Town',
'WM' : 'World Map',
'CA' : 'Port Royal',
'TR' : 'Space Paranoids',
'EH' : 'The World That Never Was',
'ZZ' : 'Empty World',
'??' : 'IDK',
}
worldsToNum = {
    0 : "ZZ",
 1  : 'ES',
 2  : 'TT',
 3  : 'DI',
 4  : 'HB',
 5  : 'BB',
 6  : 'HE',
 7  : 'AL',
 8  : 'MU',
 9  : 'PO',
 0xa : 'LK',
 0xb : 'LM',
 0xc : 'DC',
 0xd : 'WI',
 0xe : 'NM',
 0xf : 'WM',
 0x10 : 'CA',
 0x11 : 'TR',
 0x12 : 'EH',
 100 : '??',
 101 : '??',
 102 : '??',
 110 : '??',
}
CharacterNumbersToStr = {
 0 : "Sora",
 1  : 'Donald',
 2  : 'Goofy',
 3  : 'Mickey',
 4  : 'Auron',
 5  : 'Ping',
 6  : 'Aladdin',
 7  : 'Sparrow',
 8  : 'Beast',
 9  : 'Jack',
 10 : 'Simba',
 11 : 'Tron',
 12 : 'Riku',
 0xD : 'Roxas',
}

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)() # retain local pointer to value
        return value                     # faster to return than dict lookup
outcomeList_Worlds = Vividict()
outcomeList_CharacterBonusLevel = Vividict()
outcomeList_CharacterLevelUps = Vividict()
outcomeList_ItemShop = Vividict()
chestOutcomeList =Vividict()
stringFormatSize = "{:<40}"
def writeOutCome_Enemy(world,room,uid,org,new,groupname):
    orgName =  "???"
    for x in enemy_table:
        if(enemy_table[x][1] == org):
            orgName = x
    outcomeList_Worlds[worldsToText[world.upper()]][room][0][groupname][uid] = "OLD ENEM:" + stringFormatSize.format(orgName) + " NEW ENEM:" + stringFormatSize.format(new)
def writeOutCome_Boss(world,room,uid,org,new,groupname):
    orgName =  "???"
    for x in boss_table:
        if(boss_table[x][1] == org):
            orgName = x
    outcomeList_Worlds[worldsToText[world.upper()]][room][0][groupname][uid] = "OLD BOSS:" + stringFormatSize.format(orgName) + " NEW BOSS:" + stringFormatSize.format(new)
def writeOutCome_SuperBoss(world,room,uid,org,new,groupname):
    orgName =  "???"
    for x in superBoss_table:
        if(superBoss_table[x][1] == org):
            orgName = x
    outcomeList_Worlds[worldsToText[world.upper()]][room][0][groupname][uid] = "OLD SUPRBOSS:" + stringFormatSize.format(orgName) + " NEW SUPRBOSS:" + stringFormatSize.format(new)
def writeOutCome_Ally(world,room,uid,org,new,groupname):
    orgName =  ""
    for x in ally_table:
        if(ally_table[x][1] == org):
            orgName = x
    for x in ally_table:
        if(ally_table[x][1] == new):
            new = x
    outcomeList_Worlds[worldsToText[world.upper()]][room][0][groupname][uid] = "OLD ALLY:" + stringFormatSize.format(orgName) + " NEW ALLY:" + stringFormatSize.format(new)


def writeOutCome_Chest(world,room,type,uid,org,new):
    #damn i suck at coding lmao
    chestOutcomeList[worldsToText[worldsToNum[world]]][room][1 + type][uid] = "OLD CHESTITEM:" + stringFormatSize.format(org) + " NEW CHESTITEM:" + stringFormatSize.format(new)
def writeOutCome_BonusLevel(char,level,string):
    #damn i suck at coding lmao
    outcomeList_CharacterBonusLevel[char][level]= string
def writeOutCome_ItemShop(num,string):
    #damn i suck at coding lmao
    outcomeList_ItemShop[num]= string
def writeOutCome_LevelUps(char,level,string):
    #damn i suck at coding lmao
    outcomeList_CharacterLevelUps[char][level]= string

def printOutComeText():
    def writeATab(tabs):
        for i in range(tabs):
            file.write("\t")


    if (os.path.isfile("randomOutcome.txt")):
        os.remove("randomOutcome.txt")
    file = open("randomOutcome.txt","w")
    file.write("Version:" + str(version.applicationversion) +'\n')
    file.write("Seed:" + str(settings.internalSeed) + '\n')
    file.write("Enemies:" + "\n")
    for x in outcomeList_Worlds:
        writeATab(1)
        file.write("WORLD:" + x + "\n")
        for r in outcomeList_Worlds[x]:
            writeATab(2)
            file.write("ROOMNUM:" + str(r) + "\n")
            for enem in outcomeList_Worlds[x][r]:
                writeATab(3)
                file.write("TYPE:" + str(enem) + "\n")
                for groupname in outcomeList_Worlds[x][r][enem]:
                    writeATab(4)
                    file.write("GROUPNAME:" + groupname + "\n")
                    for ud in outcomeList_Worlds[x][r][enem][groupname]:
                        writeATab(5)
                        file.write("UniqueID:" + str(ud) + "\n")
                        writeATab(6)
                        file.write("OUTPUTTED:" + outcomeList_Worlds[x][r][enem][groupname][ud] + "\n")
    file.write("Chests:" + "\n")
    for x in chestOutcomeList:
        writeATab(1)
        file.write("WORLD:" + x + "\n")
        for r in sorted(chestOutcomeList[x]):
            writeATab(2)
            file.write("ROOMNUM:" + str(r) + "\n")
            for enem in sorted(chestOutcomeList[x][r]):
                writeATab(3)
                file.write("TYPE:" + str(enem) + "\n")
                for ud in sorted(chestOutcomeList[x][r][enem]):
                    writeATab(4)
                    file.write("UniqueID:" + str(ud) + "\n")
                    writeATab(5)
                    file.write("OUTPUTTED:" + chestOutcomeList[x][r][enem][ud] + "\n")
    file.write("Character Bonus Levels:" + "\n")
    for x in sorted(outcomeList_CharacterBonusLevel):
        writeATab(1)
        file.write("Character:" + CharacterNumbersToStr[x] + "\n")
        for r in sorted(outcomeList_CharacterBonusLevel[x]):
            writeATab(2)
            oldR = r
            r = str(r)
            if oldR >= 200:
                r = "Drive Ability"
            if oldR >= 300:
                r = "CriticalBonus Ability"


            file.write("LVL:" + "{:<4}".format(r) +":" +outcomeList_CharacterBonusLevel[x][oldR] + "\n")
    file.write("Character Level Ups:" + "\n")
    for x in sorted(outcomeList_CharacterLevelUps):
        writeATab(1)
        file.write("Character:" + CharacterNumbersToStr[x] + "\n")
        for r in sorted(outcomeList_CharacterLevelUps[x]):
            writeATab(2)
            file.write("LVL:" + "{:<4}".format(str(r)) +":" +outcomeList_CharacterLevelUps[x][r] + "\n")
    file.write("Item Shop Data:" + "\n")
    for x in sorted(outcomeList_ItemShop):
        writeATab(1)
        file.write("Shop Item " +str(x) +  ":" + outcomeList_ItemShop[x] + "\n")

    file.close()