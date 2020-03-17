import os
import os.path
import shutil
import settings
from utils import ErrorWindow, writeRandomizationLog, readAndUnpack, readHex, writeIntOrHex,copyKHFile,PS3Version
from kh2rando_binUtils import findBarHeader,findHeaderinBAR,ModifyExtraFileNames
class KHMapReplacer:
    def ReplaceMAP(self,MapReplaced,MapReplacer): #MapReplacer == filename of old map (no .bar), MapReplaced == filename of new map (no .bar)
        #PS3 version has all the maps in one singular folder for all regions while kh2fm has it in the JP folder
        fileExtension = '.map'
        importFolderName = "export/KH2/map/"
        if PS3Version():
            importFolderName = "export/map/"
        exportFolderName = "map/jp/"
        if PS3Version():
            exportFolderName = "map/"

        if (os.path.isfile(importFolderName + MapReplacer + fileExtension)):

            if not os.path.exists(exportFolderName):
                os.makedirs(exportFolderName)


            shutil.copyfile(importFolderName + MapReplacer + fileExtension, exportFolderName + MapReplaced + fileExtension)
            print("Copying file...")
            writeRandomizationLog(exportFolderName + MapReplaced + fileExtension)

            fileBin = open(exportFolderName + MapReplaced + fileExtension, 'rb+')  # Modify file to use correct bonus level.
            ModifyExtraFileNames(fileBin,  MapReplacer,MapReplaced)
            fileBin.close()