#Replace text ingame with some randomizer info
import kh2rando_textTable
import os
import os.path
from kh2rando_textMain import openKHText,closeKHText
import settings
from version import applicationversion
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack, readHex, writeIntOrHex,copyKHFile,PS3Version
def TwilightTownTutText():
    file = "msg/jp/tt.bar"
    if PS3Version():
        file = "msg/us/tt.bar"
    if copyKHFile(file):
        strings = openKHText(file)

        messageIDS = []

        msg1 = "Welcome to the {0x04}{0x02}KH2 Randomizer! {0x04}{0x03}" + "{lf}"
        msg1 += "Your current seed is:{0x04}{0x02}" + str(settings.internalSeed) + "{0x04}{0x03}." + "{lf}"
        msg1 += "Current Version: {0x04}{0x02}" + str(applicationversion) + "{0x04}{0x03}. {eol}"
        msg2 = "Current Settings: " + "{lf}"
        msg3 = "Notes: " + "{cls}"
        msg3+= "●Missable items in the prologue{lf}are not randomized to prevent{lf}missing key items.{cls} "
        msg3+= "●Do not equip any keyblades before gaining a drive bar.{cls}If you equip a keyblade before then,{lf}you run the risk of losing that keyblade."
        if not PS3Version():
            msg3+="{cls}"
            msg3+= "●Occasionally, the game will run low on memory.{lf} You can tell by viewing a tutorial in the pause menu{lf} or seeing your limit command flash repeatedly.{cls}" \
               " When this happens, the game may crash/softlock IF:{lf} you use mickey, go into a drive form,{lf} change party members, or anything possibly taxing."
        else:
            msg3 += "{cls}"
            msg3 += "Since we're running on the PS3 Version of the game,{lf}we have more memory to work with.{lf}There is no need to play cautiously for memory."

        msg3+="{eol}"
        msg4 = "You may now equip any {0x04}{0x02}keyblades{0x04}{0x03} you have safely.{eol}"
        linesWrote = 0
        for x in settings.config["variables"]:
            if linesWrote < 12:
                msg2 += str(x) + " : " +str(settings.config["variables"][x]) + "{lf}"
                linesWrote+=1
            else:
                msg2 +='{cls}'
                linesWrote = 0
        for x in settings.config["intvars"]:
            if linesWrote < 12:
                msg2 += str(x) + " : " +str(settings.config["intvars"][x]) + "{lf}"
                linesWrote+=1
            else:
                msg2 +='{cls}'
                linesWrote = 0
        msg2 += '{eol}'
        x= 0
        for datastring in strings:

            datastring.decryptText()
            if "Move the left " in datastring.pureString and "make Roxas run." in datastring.pureString:
                datastring.text = msg1
            if "By skimming the sides of buildings," in datastring.pureString:
                datastring.text = msg2
            if "Reaction commands are used to" in datastring.pureString:
                datastring.text = msg3
            if "Drive command has been added" in datastring.pureString:
                datastring.text = msg4
            x += 1
        closeKHText(file, strings)
def worldMapGummiShipTxtSkip():
    file = "msg/jp/wm.bar"
    if PS3Version():
        file = "msg/us/wm.bar"
    if copyKHFile(file):
        strings = openKHText(file)

        messageIDS = []

        msg1 = "To skip gummiship missions, simply fly to the world and enter.{lf} It may seem locked but it isn't." + "{cls}"
        msg1 += "Be sure to visit every world when possible{lf} to unlock them before revisting the worlds on the second visit." + "{eol}"
        for datastring in strings:
            datastring.decryptText()
            if datastring.pureString.find("Gummi Route") != -1:
                datastring.text = msg1
        closeKHText(file, strings)