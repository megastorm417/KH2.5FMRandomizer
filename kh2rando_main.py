import random
import os, os.path
import sys
import settings as cfg
from utils import PS3Version
import shutil
import utils
import traceback
import kh2rando_randomArdFiles
import kh2rando_chests
import kh2rando_shops
import kh2rando_levelRandom
import kh2rando_itemDrop
import kh2rando_equipmentRandom
from kh2rando_chests import RandomizeChestContents
from kh2rando_randomArdFiles import RandomizeARD,randomizeMusic,removeEnemySpawnLimit
from kh2rando_levelRandom import RandomizeBonusLevels,RandomizeLevelUps,ReduceFormGrinding,RandomizeDriveFormAbilities,RandomizeCriticalBonusAbilities
from kh2rando_writeRandoOutcome import printOutComeText
from kh2rando_miscAdjustments import setSoraPartyMembers,skipGummiShipMissions,giveHUDElements
from kh2rando_gameTextInfo import TwilightTownTutText,worldMapGummiShipTxtSkip
from kh2rando_itemDrop import randomizeItemDrops
from kh2rando_equipmentRandom import randomizeEquipmentStats
import gui
"""
PS3 Differences
Big Endian, has extra file data at top of header, some strings are swapped for big endian compatability some arent.
"""
def extractKH2Files(force = False):

    if not PS3Version():
        if(os.path.isfile('KH2FM_Toolkit.exe') and (not os.path.isdir('export') or force)):
            if (cfg.config["variables"].getboolean("EnglishPatch")):
                optionalString = " \"" + cfg.config["strings"]["EnglishPatchFile"].rstrip() + "\""
                os.system("KH2FM_Toolkit" + + cfg.config["strings"]["baseRom"] +" -batch" + optionalString)
                os.system("KH2FM_Toolkit -extractor -batch " + os.path.dirname(cfg.config["strings"]["baseRom"]) + '/KH2.NEW.ISO');
                print("Extraction complete.")
            else:
                os.system("KH2FM_Toolkit -extractor -batch " + cfg.config["strings"]["baseRom"]);
                print("Extraction complete.")
            return True
        else:
            if(not os.path.isfile('KH2FM_Toolkit.exe')):
                utils.ErrorWindow("No KH2FM_Toolkit.exe found! It must be in the same folder.")
                return False
            else:
                return True
    else:
        if (os.path.isfile('HasherHD.exe') and (not os.path.isdir('export') or force)):
            if os.path.isfile('index.dat'):
                os.system("HasherHD.exe --batch --extractmself index.dat " + cfg.config["strings"]["baseRom"])  # Patch AFTER the english because it changes some things
                print("Extraction complete.")
                return True
            else:
                utils.ErrorWindow("No index.dat found! It must be in the same folder.")
                return False
        else:
            if not os.path.isfile('HasherHD.exe'):
                utils.ErrorWindow("No HasherHD.exe found! It must be in the same folder.")
                return False
            else:
                return True

        
def forceExtractKh2Files():
    #mainly used for gui.
    extractKH2Files(True)
    
def initAllVars():
    kh2rando_shops.initVar()
    kh2rando_randomArdFiles.initVar()
    kh2rando_levelRandom.initVar()
    kh2rando_chests.initVar()
    kh2rando_itemDrop.initVar()
    kh2rando_equipmentRandom.initVar()
def createNewPatch():
    if not PS3Version():
        randomLogName = "randomizationLog.txt"
        randomLog = open(randomLogName,"a")
        utils.writeNewline(randomLog,"")
        utils.writeNewline(randomLog,"")
        randomLog.write("")
        randomLog.close()
        #Delete KH2 Patch!!! Otherwise toolkit will not overwrite it :(
        if(os.path.exists("output.kh2patch")):
            os.remove("output.kh2patch")
        CommandLineString = "KH2FM_Toolkit.exe -patchmaker -batch -version 1 -author AutoBatch -skipchangelog -skipcredits -other GovanifYAutoBatch -uselog randomizationLog.txt"
        os.system(CommandLineString);
    
def createNewIsoWithPatch():
    if not PS3Version():
        optionalString = "";
        if(cfg.config["variables"].getboolean("EnglishPatch")):
            optionalString = " \""+cfg.config["strings"]["EnglishPatchFile"].rstrip() + "\""
        os.system("KH2FM_Toolkit "+cfg.config["strings"]["baseRom"]+ " -batch" + optionalString + " output.kh2patch") #Patch AFTER the english because it changes some things
        newName = "KH2FMRandom_Seed_" + str(cfg.internalSeed)
        filetype = ".ISO"
        #while os.path.isfile(cfg.config["strings"]["romDirSelect"].rstrip() + newName + filetype):
            #newName += "_Copy"
        print("created new Iso called:" + newName)
        #os.rename("KH2FM.NEW.ISO",newName + filetype)
        try:
            if (cfg.config["strings"]["romDirSelect"]).rstrip() != "":
                print("Moving/Renaming KH2FM to new Directory....")
                shutil.move(os.path.dirname(cfg.config["strings"]["baseRom"]) + '/KH2FM.NEW.ISO',(cfg.config["strings"]["romDirSelect"]).rstrip() + '/' + newName + filetype)
        except Exception:
            print("Unable to move/rename to new Directory!!!")
    else:
        if os.path.isfile('HasherHD.exe') :
            if os.path.isfile('index.dat'):
                os.system("HasherHD.exe --batch --createNewMSelf index.dat " + cfg.config["strings"]["baseRom"])
            else:
                utils.ErrorWindow("An index.dat is not found! It must be in the same folder as this program. It can be found in the same folder as the .mself file.")
        else:
            utils.ErrorWindow("HasherHD.exe not found! It must be in the same folder as this program.")
    
def setSeed(seed):
    if(seed == ""):
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    cfg.internalSeed = seed
    
    
def prepareRandomizationLog():
    if not PS3Version():
        if(os.path.isfile("randomizationLog.txt")):
            os.remove("randomizationLog.txt")
    else:
        if (os.path.isfile("UsedLog.log")):
            os.remove("UsedLog.log")
    utils.randomLogFirstTime = True
    utils.clearLogsWroteSoFar()
def CleanUPRandomizedFiles():
    #We should clean up before randomizing again so that we can start fresh
    for file in utils.logsWroteSoFar:
        os.remove(file)

def randomizeNewRun():
    try:
        if cfg.config["strings"]["baseRom"] != "" and cfg.config["strings"]["romDirSelect"] != "":
            setSeed(cfg.config["strings"]["seed"])
            print('Starting Seed:' + str(cfg.internalSeed))
            prepareRandomizationLog()
            initAllVars()
            gui.setProgressBar(10)
            if(extractKH2Files()):
                TwilightTownTutText()
                if cfg.config["variables"].getboolean("SkipGummishipMission"):
                    worldMapGummiShipTxtSkip()
                RandomizeChestContents(cfg.config["variables"].getboolean("RandomizeChestItems"))
                kh2rando_shops.randomizeShops(cfg.config["variables"].getboolean("RandomItemShops"))
                gui.setProgressBar(20)
                RandomizeARD(cfg.config["variables"].getboolean("RandomizeEnemies"),
                             cfg.config["variables"].getboolean("RandomizeBosses"),
                             cfg.config["variables"].getboolean("RandomizeAllies"),
                             cfg.config["variables"].getboolean("KH2SoraForced"),
                             cfg.config["variables"].getboolean("EnemyOptimizations"),
                             cfg.config["intvars"].getint("SuperBossEncounterRate"))
                randomizeMusic(cfg.config["variables"].getboolean("RandomizeMusic"))
                randomizeItemDrops(cfg.config["variables"].getboolean("RandomizeItemDrop"),cfg.config["variables"].getboolean("RandomizeItemDropPercentage"))
                randomizeEquipmentStats(cfg.config["variables"].getboolean("RandomizeEquipmentStats"),cfg.config["variables"].getboolean("RandomizeEquipmentAbilities"))
                removeEnemySpawnLimit(cfg.config["variables"].getboolean("RandomizeEnemies"))
                skipGummiShipMissions(cfg.config['variables'].getboolean("SkipGummishipMission"))
                #giveHUDElements()
                setSoraPartyMembers(cfg.config["variables"].getboolean("KH2SoraForced"))
                gui.setProgressBar(40)
                RandomizeBonusLevels(cfg.config["variables"].getboolean("RandomizeBonusLevelsAndAbilities"),
                                     cfg.config["variables"].getboolean("RandomizeBonusItems"),
                                     cfg.config["variables"].getboolean("RandomizeCritBonusAbilities"),
                                     cfg.config["intvars"].getint("RandomAbilityAmount"),
                                     cfg.config["variables"].getboolean("GuardFirst"))
                RandomizeDriveFormAbilities(cfg.config["variables"].getboolean("RandomizeBonusLevelsAndAbilities"))
                RandomizeCriticalBonusAbilities(cfg.config["variables"].getboolean("RandomizeBonusLevelsAndAbilities"),cfg.config["variables"].getboolean("RandomizeCritBonusAbilities"))
                RandomizeLevelUps(cfg.config["variables"].getboolean("RandomizeLevelUps"))
                gui.setProgressBar(50)
                ReduceFormGrinding(cfg.config["variables"].getboolean("ReduceDriveForm"))
                gui.setProgressBar(60)
                gui.setProgressBar(70)
                if cfg.config["variables"].getboolean("OutcomeTextFile"):
                    printOutComeText()

                createNewPatch()
                if not cfg.config["variables"].getboolean("CreateOnlyPatch"):
                    gui.setProgressBar(80)
                    createNewIsoWithPatch()
                    gui.setProgressBar(90)
                    gui.setProgressBar(100)
                    PS3String = ""
                    if PS3Version():
                        PS3String = "\nBe sure to move the .NEW.mself file and index.NEW.dat into the game directory and rename the old game files."
                    utils.GeneralMessageWindow("All done!!!\nIt was put in \n" + cfg.config["strings"]["romDirSelect"].rstrip() +"\nwith the seed:" + str(cfg.internalSeed) + PS3String ,"Randomization Complete!")
                else:
                    gui.setProgressBar(100)
                    PatchMessage ="A patch was created in the directory of this program."
                    if PS3Version():
                        PatchMessage = "An outcome was created."
                    utils.GeneralMessageWindow(PatchMessage, "Randomization Complete!")
                print('Randomization Complete.')
        else:
            utils.ErrorWindow("Error: Either the base rom or the directory is not set yet.")
    except Exception as e:
        traceback.print_exc()
        utils.ErrorWindow("An error has occured during the randomization!")

    CleanUPRandomizedFiles()
    gui.turnBackOnRandoButton()


    
