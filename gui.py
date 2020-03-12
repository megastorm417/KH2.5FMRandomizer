from tkinter.filedialog import *
from tkinter import *
from tkinter.ttk import *
import threading
import queue
import settings as cfg
from utils import PS3Version
import version
from kh2rando_main import randomizeNewRun,forceExtractKh2Files
#from utils import ErrorWindow
guiVars = {}

def setProgressBar(value):
     progressBar['value'] = value;
def turnBackOnRandoButton():
     buttonStartRandom['state'] = NORMAL;


class ToolTip:

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
            
            
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class TemporaryTextForEntry:
    def __init__(self, widget,text):
        self.widget = widget
        self.text = text;
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        if (self.widget.get() == ''):
            self.widget.insert(0, self.text)
            self.widget.config(foreground = 'gray')
        
    def on_entry_click(self):
        if (self.widget.get() == self.text):
            self.widget.delete(0, "end") # delete all the text in the entry
            self.widget.insert(0, '') #Insert blank for user input
            self.widget.config(foreground = 'black')
       
    def on_focusout(self):
        if (self.widget.get() == ''):
            self.widget.insert(0, self.text)
            self.widget.config(foreground = 'gray')
        else:
            self.widget.config(foreground = 'black')


        
def TempTextForEntry(widget,text):
    TText = TemporaryTextForEntry(widget,text)
    def focusin(event):
        TText.on_entry_click()
    def focusout(event):
        TText.on_focusout()
    widget.bind('<FocusIn>', focusin)
    widget.bind('<FocusOut>', focusout)
    
    
def mainGui():
    miscTogglesSize = 0
    def guiVarsToSave():
        for x in cfg.config["strings"]:
            cfg.config["strings"][x] = guiVars[x].get()
        for x in cfg.config["variables"]:
            cfg.config["variables"][x] = str(guiVars[x].get())
        for x in cfg.config["intvars"]:
            cfg.config["intvars"][x] = str(guiVars[x].get())

        cfg.saveSettings()
        return True
    def makeGuiVars():
        for x in cfg.config["strings"]:
            guiVars[x] = StringVar(currentBase)
            guiVars[x].set(cfg.config["strings"][x])
        for x in cfg.config["variables"]:
            guiVars[x] = BooleanVar(currentBase)
            guiVars[x].set(cfg.config["variables"][x])
        for x in cfg.config["intvars"]:
            guiVars[x] = IntVar(currentBase)
            guiVars[x].set(cfg.config["intvars"][x])

    def output_dir_select():
        fileGotton = filedialog.askdirectory()
        fileGotton = fileGotton.rstrip()
        if fileGotton != '':
            guiVars['romDirSelect'].set(fileGotton)
            guiVarsToSave()

    def baseiso_open():
        if not PS3Version():
            fileGotton = filedialog.askopenfilename(initialdir="/", title="Open Base KH2ISO file",
                                                    filetypes=[("ISO file", "*.iso")])
        else:
            fileGotton = filedialog.askopenfilename(initialdir="/", title="Open Base KH2.5 file",
                                                    filetypes=[("MSELF file", "*.mself")])
        fileGotton = fileGotton.rstrip()
        if fileGotton != '':
            guiVars['baseRom'].set(fileGotton)
            guiVarsToSave()


    def openEnglishPatch():
        fileGotton = filedialog.askopenfilename(initialdir="/", title="Open KH2FM English Patch",
                                                filetypes=[("Kingdom hearts patch file", "*.kh2patch")])
        fileGotton = fileGotton.rstrip()
        if fileGotton != '':
            guiVars['EnglishPatchFile'].set(fileGotton)
            guiVarsToSave()

    def createARandomizeToggleButton(tab,ButtonText,guiVar,tooltiptext,row2,column2):
        newButt = Checkbutton(tab, text=ButtonText,var=guiVars[guiVar], command=guiVarsToSave)
        CreateToolTip(newButt,text=tooltiptext)
        newButt.grid(row = row2, column = column2,sticky = "W")
    def createARandomizeRadButton(tab,ButtonText,guiVar,buttValue,tooltiptext,row2,column2):
        newButt = Radiobutton(tab, text=ButtonText,var=guiVars[guiVar], command=guiVarsToSave,value=buttValue)
        CreateToolTip(newButt,text=tooltiptext)
        newButt.grid(row = row2, column = column2,sticky = "W")

    def startANewRandomization():
        buttonStartRandom['state'] = DISABLED
        progressBar['value'] = 0;
        newQueue = queue.Queue()
        newTask = ThreadedTask(newQueue,randomizeNewRun)
        newTask.start()
    def mainToggles():
        listItemNum = 0
        createARandomizeToggleButton(frames['MainToggles'],
                                    "Randomize Enemies",
                                    'RandomizeEnemies',
                                    'Randomize the enemy pool?',
                                    listItemNum, 0)
        listItemNum+=1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Bosses",
                                     'RandomizeBosses',
                                     'Randomize the bosses?',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Allies",
                                     'RandomizeAllies',
                                     'Randomize Allies?',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                    "Randomize Items",
                                    'RandomizeChestItems',
                                    'Randomizes chests and event items.\nItems from roxas\'s prologue are not randomized.',
                                    listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Item Shops",
                                     'RandomItemShops',
                                     'Randomize shop keepers item inventory.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Bonus Levels and Abilities",
                                     'RandomizeBonusLevelsAndAbilities',
                                     'Randomizes all bonus levels and abilities you obtain such as defeating a boss and Drive form abilities.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Critical Bonus Abilities",
                                     'RandomizeCritBonusAbilities',
                                     'Randomize critical bonus abilities. Disable for consistent strong abilities.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Give Extra Bonus Items On Bonus LevelUp",
                                     'RandomizeBonusItems',
                                     'Get bonus items when possible with bonus levels.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Level Ups",
                                     'RandomizeLevelUps',
                                     'Randomize player & party levelups.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Item Drop",
                                     'RandomizeItemDrop',
                                     'Randomize item drops from enemies.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Item Drop %",
                                     'RandomizeItemDropPercentage',
                                     'Randomize item drop percentages from enemies.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Equipment Stats",
                                     'RandomizeEquipmentStats',
                                     'All equipment stats will be randomized.\n(AP, Strength, Magic, Defense, Physical resistance, \nFire Resist, Blizzard Resist, Thunder Resist, Dark Resist)',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MainToggles'],
                                     "Randomize Equipment Abilities",
                                     'RandomizeEquipmentAbilities',
                                     'All equipment abilities will be randomized.',
                                     listItemNum, 0)
        listItemNum += 1


    def miscToggles():
        nonlocal miscTogglesSize
        listItemNum = 0

        createARandomizeToggleButton(frames['MiscToggles'],
                                     "Randomize Music",
                                     'RandomizeMusic',
                                     'Randomizes MOST of the music in the game.\nNOTE: This unfortunately affects game stability in some scenarios.',
                                     listItemNum, 0)
        listItemNum+=1

        createARandomizeToggleButton(frames['MiscToggles'],
                                     "Force KH2Sora for prologue",
                                     'KH2SoraForced',
                                     'Replace Roxas/KH1Sora with KH2Sora for the prologue except for when Roxas is needed to progress.\nAllows for use of reaction commands against enemies and other specific Sora things',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MiscToggles'],
                                     "Reduced Drive Form Grinding",
                                     'ReduceDriveForm',
                                     'Reduce drive form grinding. Helps for quick random runs.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MiscToggles'],
                                     "Guarantee Guard Ability",
                                     'GuardFirst',
                                     'Get guard as your first ability.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MiscToggles'],
                                     "Skip gummiship missions",
                                     'SkipGummishipMission',
                                     'Skip gummiship missions.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeToggleButton(frames['MiscToggles'],
                                     "PS2 enemy optimiziation",
                                     'PS2EnemyOptimizations',
                                     'While this is on, enemies are categorized into low, medium and high memory objects.\nTurn this off if you want completely random enemies for every spawn.\nHowever, Turning this off is not recommended for PS2 as it may crash on room loads and other bugs.',
                                     listItemNum, 0)
        listItemNum += 1
        miscTogglesSize = listItemNum
    def AdditionalButtons():
        listItemNum = 0
        createARandomizeRadButton(frames['AdditionalButtons'],
                                     "Normal Ability Amount",
                                     'RandomAbilityAmount',
                                    1,
                                     'A normal amount of abilities.',
                                     listItemNum, 0)
        listItemNum += 1
        createARandomizeRadButton(frames['AdditionalButtons'],
                                     "Extra Abilities",
                                     'RandomAbilityAmount',
                                    2,
                                     'An extra amount of abilities more than the base game gives. \nGives the most possible through bonus levels. \nOnly abilities that stack are added aswell.',
                                     listItemNum, 0)
        listItemNum += 1
    def creditToggles():
        listItemNum = 0
        CreditLabel = Label(currentBase, text="Credits/Special Thanks:")
        CreditLabel.grid(row=listItemNum, column=0, sticky="W")
        listItemNum += 1
        CreditLabel = Label(currentBase, text="KH2FM Modding community's documentary of KH2FM Data.")
        CreditLabel.grid(row=listItemNum, column=0, sticky="W")
        listItemNum += 1
        CreditLabel = Label(currentBase, text="Govanify's KH2FM patch toolkit.")
        CreditLabel.grid(row=listItemNum, column=0, sticky="W")
        listItemNum += 1
        CreditLabel = Label(currentBase, text="CrazyCatz00's HasherHD original program and KH2 Text to Hex tables.")
        CreditLabel.grid(row=listItemNum, column=0, sticky="W")
        listItemNum += 1
        CreditLabel = Label(currentBase, text="TruthKey's original randomizer code.")
        CreditLabel.grid(row=listItemNum, column=0, sticky="W")
        listItemNum += 1

    frames = {}
    main_Window = Tk()
    #main_Window.resizeable(0,0)
    main_Window.wm_title("KH2Randomizer " + version.applicationversion)
    main_Window.wm_resizable(0,0)
    
    #KH_Label = Label(main_Window,text = "KH2Randomizer")
    #KH_Label.pack()
    frames['OuterFrame'] = Frame(main_Window)
    frames['OuterFrame'].pack(side=BOTTOM)
    notebook_kh = Notebook(main_Window,width=448,height=312,padding=5)
    notebook_kh.pack()
    #frames['randomizeTab'] = ttk.Frame(notebook)
    frames['optionTab'] = Frame(notebook_kh, relief=RIDGE, borderwidth=3)
    frames['creditsTab'] = Frame(notebook_kh, relief=RIDGE, borderwidth=3)
    frames['randomizeTab'] = Frame(notebook_kh, relief=RIDGE, borderwidth=3)
    iconFile = "icon.ico"
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    elif __file__:
        base_path = os.path.dirname(__file__)
    main_Window.iconbitmap(default=(os.path.join(base_path,iconFile)))
    #Exitbutton = Button(frames['randomizeTab'],text="Exit",command=main_Window.destroy)
    #Exitbutton.grid(row=0,column = 0)
    """Write to outer frame of direction and randomize button """
    frames['Directories'] = LabelFrame(frames['OuterFrame'],text="Output",labelanchor=NW)
    currentBase = frames['Directories'];
    global buttonStartRandom,progressBar
    buttonStartRandom = Button(currentBase,text="Randomize",command=startANewRandomization)
    buttonStartRandom.grid(row=0,column = 1)
    progressBar = Progressbar(currentBase,orient = HORIZONTAL, length=200,mode='determinate')
    progressBar.grid(row=0,column = 2)

    makeGuiVars()
    
    
    button_baseRom = Button(currentBase,text="Set base ROM",command=baseiso_open)
    button_baseRom.grid(row=1,column = 1)
    baseRomEntry = Entry(currentBase,width=50,textvariable = guiVars['baseRom'],validate="focusout",validatecommand=guiVarsToSave)
    baseRomEntry.grid(row=1,column = 2)
    #TempTextForEntry(baseRomEntry,"KH2FM.ISO")

    
    button_baseRomDir = Button(currentBase,text="Set randomized ROM Directory",command=output_dir_select)
    button_baseRomDir.grid(row=3,column = 1)
    baseRomDirEntry = Entry(currentBase,width=50,textvariable = guiVars['romDirSelect'],validate="focusout",validatecommand=guiVarsToSave)
    baseRomDirEntry.grid(row=3,column = 2)
    
    seedLabel = Label(currentBase,text="Seed:")
    seedLabel.grid(row=4,column = 1,sticky = "E")
    seedEntry = Entry(currentBase,width=50,textvariable = guiVars['seed'],validate="focusout",validatecommand=guiVarsToSave)
    seedEntry.grid(row=4,column = 2,sticky = "W")
    CreateToolTip(seedEntry, text='Enter a seed. Leave blank for random.')
    createARandomizeToggleButton(currentBase,
                                 "Create seed outcome textfile",
                                 'OutcomeTextFile',
                                 'Show what is in the seed on randomization.',
                                 5, 1)

    createARandomizeRadButton(currentBase,
                              "PS2 Version",
                              'CurrentGameVersion',
                              0,
                              'Lower memory amount than PS3 Version, smaller filesize.\nUses .ISO files.',
                              5, 2)
    createARandomizeRadButton(currentBase,
                              "PS3 Version",
                              'CurrentGameVersion',
                              1,
                              'Higher memory than the PS2 Version.\nHowever, the item shop cannot be randomized\nand sometimes bosses crash the game\nwhere it doesn\'t on the PS2 Version.(Atleast on RCPS3 ATM).\nUses .MSELF files.\nUses US/PAL region for now.',
                              6, 2)

    createARandomizeToggleButton(currentBase,
                                 "Create Patch/Outcome only",
                                 'CreateOnlyPatch',
                                 'Create only a patch. Must be manually applied.\nIf a PS3 version is selected, it will only create an outcome.',
                                 6, 1)
    #TempTextForEntry(seedEntry,"Enter a seed. Leave blank for random.")
    frames['Directories'].pack(side=BOTTOM)
    frames['MainToggles'] = LabelFrame(frames['randomizeTab'], text="Main Toggles", labelanchor=NW)
    frames['MiscToggles'] = LabelFrame(frames['randomizeTab'], text="Misc", labelanchor=NW)
    frames['AdditionalButtons'] = LabelFrame(frames['MiscToggles'], text="Additional", labelanchor=NW)
    """Add options to toggle on randomization of certain things, such as bosses """
    mainToggles()
    miscToggles()
    AdditionalButtons()

    frames['MainToggles'].grid(row = 0 ,column = 0,sticky = "NW")
    frames['MiscToggles'].grid(row = 0 ,column = 1,sticky = "NW")
    frames['AdditionalButtons'].grid(row = miscTogglesSize ,column = 0,sticky = "NW")
    frames['randomizeTab'].pack(fill=BOTH,expand=1)
    
    
    currentBase = frames['optionTab'];
    refreshExtractedFilesBut = Button(currentBase,text="Refresh extracted files",command=forceExtractKh2Files)
    refreshExtractedFilesBut.grid(row=0,column = 0,sticky = "W")
    SetEnglishPatchBut = Checkbutton(currentBase,text="Translate game when randomized",var=guiVars['EnglishPatch'],command=guiVarsToSave)
    SetEnglishPatchBut.grid(row=1,column = 0,sticky = "W")
    CreateToolTip(SetEnglishPatchBut,text= "The game will be translated to english if checked.")
    SetEnglishPatchBut = Button(currentBase,text="Set english patch",command=openEnglishPatch)
    SetEnglishPatchBut.grid(row=2,column = 0,sticky = "W")
    setEnglishPatchEntry = Entry(currentBase,width=70,textvariable = guiVars['EnglishPatchFile'],validate="focusout",validatecommand=guiVarsToSave)
    setEnglishPatchEntry.grid(row=3,column = 0,sticky = "W")
    
    #Credits
    currentBase = frames['creditsTab'];
    creditToggles()
    
    notebook_kh.add(frames['randomizeTab'], text='Randomization')
    notebook_kh.add(frames['optionTab'], text='Options')
    notebook_kh.add(frames['creditsTab'], text='Credits')
    notebook_kh.enable_traversal()
    main_Window.mainloop()
    
    
    

class ThreadedTask(threading.Thread):
    def __init__(self, queue,func):
        threading.Thread.__init__(self)
        threading.Thread.daemon =True
        self.queue = queue
        self.func = func
    def run(self):
        self.func()  # do function
        self.queue.put("Task finished")
    

