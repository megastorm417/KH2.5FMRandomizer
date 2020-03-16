#handle main text stuff
import struct
from utils import writeIntOrHex,readAndUnpack,copyKHFile
from kh2rando_binUtils import findHeaderinBAR,findBarHeader,ModifyExtraFilePosition,ReverseEndianString
from kh2rando_textTable import KH2FMTextEvt,KH2FMTextEvt_Flipped
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)() # retain local pointer to value
        return value                     # faster to return than dict lookup
class TextBar(object):

    def __init__(self,ids,position,text):
        self.ids = []
        self.ids.append(ids) #list
        self.text = text;
        self.encrypted = True;
        self.position = position
        self.pureString = "" #String without any special characters or stuff
    def addID(self,ID):
        self.ids.append(ID)
    def __len__(self):
        return len(self.text)
    def writeBackToFile(self):
        if not self.encrypted:
            self.encryptText()
        return self.text
    def decryptText(self):
        newTextString = ""
        textStringOnlyText = ""
        self.encrypted = False;
        for x in self.text:
            if x in KH2FMTextEvt:
                newTextString+= KH2FMTextEvt[x]
                if ((x > 33 and x < 100) or (x >140 and x< 232)) or x== 1 :
                    textStringOnlyText += KH2FMTextEvt[x]
                if (x == 2):
                    textStringOnlyText += ' '
            else:
                newTextString += "{" + hex(x) + "}"
        self.text = newTextString
        self.pureString = textStringOnlyText
    def encryptText(self):
        self.encrypted = True;
        self.text = list(self.text)
        addingChars =False
        charHolder = ""
        numchar = 0
        while numchar < len(self.text):
            char = self.text[numchar]
            if char == "{":
                addingChars = True

            if addingChars:
                charHolder += self.text.pop(numchar)
                numchar -=1
            if char == "}":
                addingChars = False
                numchar +=1
                self.text.insert(numchar,charHolder)
                charHolder =""
            numchar+=1
        for numchar2 in range(len(self.text)):
            if self.text[numchar2] in KH2FMTextEvt_Flipped:
                self.text[numchar2] = KH2FMTextEvt_Flipped[self.text[numchar2]]
            elif "{0x" in self.text[numchar2]:
                textFormat = self.text[numchar2][1:len(self.text[numchar2])-1]
                self.text[numchar2] = int(textFormat,0)
        self.endingLength = len(self.text)
def RemoveDuplicate(list):
    newlist = []
    for num in list:
        if num not in newlist:
            newlist.append(num)
    return newlist
def openKHText(file): #ex : file:msg/jp/tt.bar
    #open file, grab all strings, then when we finish modifying all the strings, get the length of them all and replace.
    #Unordered list with ID and Position.
    fileBin = open(file, 'rb+')
    offset = findBarHeader(fileBin)
    test = (file[len(file)-4-2:])[:2] #Find world name by removing the last 4 characters and subtracting the length to start at the world name
    findHeaderinBAR(fileBin,test,False)
    fileBin.seek(0x8, 1)  # skip header thing
    stringSize = readAndUnpack(fileBin,4)
    findHeaderinBAR(fileBin, test, True)
    startingStringTablePos = fileBin.tell()
    fileBin.seek(0x4,1) #skip header thing
    amountOfTextLines =readAndUnpack(fileBin,4)
    stringList = []
    for x in range(amountOfTextLines):

        fileBin.seek(startingStringTablePos+ 8 + (x*8), 0)
        stringID = readAndUnpack(fileBin,4)
        stringPos = readAndUnpack(fileBin,4)
        filterStuff = list(filter(lambda x: (stringPos == x.position),stringList))
        if len(filterStuff) != 0:
            filterStuff[0].addID(stringID)
        else:
            stringList.append(TextBar(stringID, stringPos, ''))


    stringList = sorted(stringList,key=lambda x: x.position)
    fileBin.seek(startingStringTablePos + 8 + (amountOfTextLines * 8), 0)
    for x in range(len(stringList)):
        stringData = []
        currentChar = -1
        currentNextID = 1

        if x < len(stringList)-1:
            lengthOfString = (stringList[x+currentNextID].position - stringList[x].position)
            while lengthOfString > 0:
                currentChar =  readAndUnpack(fileBin,1)
                stringData.append(currentChar)
                lengthOfString-=1
        else:
            lengthOfString = ((stringSize) - stringList[x].position)
            while lengthOfString > 0:
                currentChar = readAndUnpack(fileBin, 1)
                stringData.append(currentChar)
                lengthOfString -= 1

        stringList[x].text = stringData
    fileBin.close()
    return stringList

def closeKHText(file,strings):

    fileBin = open(file, 'rb+')
    offset = findBarHeader(fileBin)
    findHeaderinBAR(fileBin, 'md_m', False)
    fileBin.seek(0x8,1)
    md_m_size = readAndUnpack(fileBin,4)
    findHeaderinBAR(fileBin, 'md_m', True)
    md_m_Data = fileBin.read(md_m_size)
    miscData = fileBin.read()
    test = (file[len(file)-4-2:])[:2] # Find world name by removing the last 4 characters and subtracting the length to start at the world name
    findHeaderinBAR(fileBin, test, True)
    startingStringTablePos = fileBin.tell()
    fileBin.seek(0x4, 1)  # skip header thing
    amountOfTextLines = readAndUnpack(fileBin, 4)
    startReadingPos = fileBin.tell()
    fileBin.seek(startingStringTablePos +8+ (amountOfTextLines*8), 0)
    for x in strings:
        x.position = fileBin.tell()-startingStringTablePos
        newList = x.writeBackToFile()
        for character in newList:
                writeIntOrHex(fileBin,character,1)

    fileEndSize = fileBin.tell()-offset
    fileBin.truncate(fileEndSize)
    newTextBarFileSize = fileEndSize- startingStringTablePos
    while fileBin.tell() % 16 != 0:
        writeIntOrHex(fileBin, 0, 1)
    newMd_mPos = fileBin.tell() -offset

    fileBin.write(md_m_Data)
    ModifyExtraFilePosition(fileBin, fileBin.tell()) #we want relative positions to 0,0 of the file.
    fileBin.write(miscData)
    fileBin.seek(startReadingPos, 0) #Go back to the start with ids and positions
    for x in strings:
        stringID = readAndUnpack(fileBin,4)
        filterStuff = list(filter(lambda x: (stringID in x.ids), strings))
        writeIntOrHex(fileBin,filterStuff[0].position,4) #Write new positions of text
    findHeaderinBAR(fileBin, 'md_m', False)
    fileBin.seek(0x4,1)
    writeIntOrHex(fileBin,newMd_mPos,4)
    findHeaderinBAR(fileBin, test, False)
    fileBin.seek(0x8, 1)
    writeIntOrHex(fileBin,newTextBarFileSize,4)
    fileBin.close()



