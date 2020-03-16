import configparser
internalSeed = -1
config = configparser.ConfigParser()
config.optionxform= lambda option: option #do not lowercase variable names!!!!! silly program
config["variables"] ={
        "RandomizeBosses": True,
        "RandomizeEnemies": True,
        "RandomizeAllies": True,
        "RandomizeChestItems": True,
        "EnglishPatch": True,
        "RandomizeBonusLevelsAndAbilities" : True,
        "RandomizeLevelUps" : True,
        "RandomizeMusic" : False,
        "KH2SoraForced" : True,
        "ReduceDriveForm" : True,
        "RandomItemShops" : True,
        "OutcomeTextFile" : True,
        "CreateOnlyPatch" : False,
        "RandomizeBonusItems" : True,
        "RandomizeCritBonusAbilities" : True,
        "SkipGummishipMission" : True,
        "GuardFirst" : True,
        "EnemyOptimizations" : True,
        "RandomizeItemDrop" : True,
        "RandomizeItemDropPercentage" : True,
        "RandomizeEquipmentStats" : True,
        "RandomizeEquipmentAbilities" : True,
    }
config['intvars'] = {

#radio button
        "RandomAbilityAmount" : 1,
        "CurrentGameVersion" : 0,
        "SuperBossEncounterRate" : 0,


}
config["strings"] ={
        "baseRom": "",
        "romDirSelect": "",
        "EnglishPatchFile": "",
        "seed": "",

}



def saveSettings():
    f = open("settings.dat", "w")
    config.write(f)
    #for x in config["variables"]:
        #writeNewline(f, str(config["variables"][x]))

    #for x in config["strings"]:
        #writeNewline(f, config["strings"][x])

    f.close()


def loadSettings():
    config.read("settings.dat")
    #for x in config["variables"]:
        #config["variables"][x] = f.readline().rstrip()

    #for x in config["strings"]:
        #config["strings"][x] = f.readline().rstrip()
