from gui import mainGui
import settings as cfg
import os, os.path
def startProgram():
    if(os.path.isfile("settings.dat")):
        cfg.loadSettings()
    mainGui()


startProgram()
