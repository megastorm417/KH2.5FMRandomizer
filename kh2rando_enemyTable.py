""" type, code,weight"""
from khenum import enemyMemoryUsage,enemyType
import random
currentType = enemyType.Normal
enemy_table = {
    'Fat Bandit':(currentType,                              0x001),
    'Trick Ghost':(currentType,                             0x002),
    'Rabid Dog':(currentType,                               0x003),
    'Hook Bat':(currentType,                                0x004,enemyMemoryUsage.Low),
    'Bookmaster':(currentType,                              0x005),
    'Aeroplane':(currentType,                               0x006,enemyMemoryUsage.Low),
    'Minute Bomb':(currentType,                             0x007,enemyMemoryUsage.Low),
    'Hammer Frame':(currentType,                            0x008),
    'Assault Rider':(currentType,                           0x009,enemyMemoryUsage.High),
    'Nightwalker':(currentType,                             0x00A),
    'Fortuneteller':(currentType,                           0x00B),
    'Luna Bandit':(currentType,                             0x00C,enemyMemoryUsage.High),
    'Hot Rod':(currentType,                                 0x00D,enemyMemoryUsage.High),
    'Cannon Gun':(currentType,                              0x00E),
    'Living Bone':(currentType,                             0x00F,enemyMemoryUsage.High),
    'Devastator':(currentType,                              0x010,enemyMemoryUsage.High),
    'Lance Soldier':(currentType,                           0x011),
    'Driller Mole':(currentType,                            0x012,enemyMemoryUsage.Low),
    'Shaman':(currentType,                                  0x013,enemyMemoryUsage.High),
    'Aerial Knocker':(currentType,                          0x014),
    'Silver Rock':(currentType,                             0x047),
    'Emerald Blues':(currentType,                           0x048,enemyMemoryUsage.High),
    'Crimson Jazz':(currentType,                            0x049,enemyMemoryUsage.High),
    'Air Pirate':(currentType,                              0x04A),
    'Bulky Vendor':(currentType,                            0x04B,enemyMemoryUsage.Low),
    'Fiery Globe':(currentType,                             0x04C,enemyMemoryUsage.Low),
    'Icy Cube':(currentType,                                0x04D,enemyMemoryUsage.Low),
    'Wight Knight':(currentType,                            0x076),
    'Wight Knight(HW)':(currentType,                        0x077),
    'Neoshadow':(currentType,                               0x078),
    #'Magnum Loader':(currentType,                          0x079),
    'Morning Star':(currentType,                            0x07A,enemyMemoryUsage.High),
    'Tornado Step':(currentType,                            0x07B,enemyMemoryUsage.Low),
    'Crescendo':(currentType,                               0x07C),
    'Creeper Plant':(currentType,                           0x07D,enemyMemoryUsage.High),
    'Soldier':(currentType,                                 0x12D),
    'Shadow (TwTown)':(currentType,                         0x12E,enemyMemoryUsage.Low),
    'Large Body':(currentType,                              0x12F,enemyMemoryUsage.High),
    'Rapid Thruster':(currentType,                          0x130),
    'Armored Knight':(currentType,                          0x131),
    'Surveillance Robot':(currentType,                      0x132),
    'Dragoon':(currentType,                                 0x134),
    'Assassin':(currentType,                                0x135),
    'Samurai':(currentType,                                 0x136),
    'Sniper':(currentType,                                  0x137,enemyMemoryUsage.High),
    'Dancer':(currentType,                                  0x138),
    'Berserker':(currentType,                               0x139,enemyMemoryUsage.High),
    'Gambler':(currentType,                                 0x13A),
    'Sorcerer':(currentType,                                0x13C,enemyMemoryUsage.High),
    'Creeper':(currentType,                                 0x13D,enemyMemoryUsage.Low),
    'Dusk':(currentType,                                    0x13E,enemyMemoryUsage.Low),
    'Gargoyle Knight':(currentType,                         0x16F,enemyMemoryUsage.High),
    'Gargoyle Warrior':(currentType,                        0x170,enemyMemoryUsage.High),
    'Strafer':(currentType,                                 0x45A,enemyMemoryUsage.Low),
    'Demyx\'s Water Clone (Norm)':(currentType,             0x4A0,enemyMemoryUsage.Low),
    'Shadow':(currentType,                                  0x4C4,enemyMemoryUsage.Low),
    'Shadow (Dif)':(currentType,                            0x555,enemyMemoryUsage.Low),
    #'Armored Knight (1,000Heartless)':(currentType,         0x5BC,enemyMemoryUsage.Low),
    #'Surveillance Robot (1,000Heartless)':(currentType,     0x5BD),
    #'Bees':(currentType,                                   0x625),
    'Bolt Tower':(currentType,                              0x627,enemyMemoryUsage.Low),
    'Fiery Globe(TreasureRoom)':(currentType,               0x686,enemyMemoryUsage.Low),
    'Icy Cube(TreasureRoom)':(currentType,                  0x687,enemyMemoryUsage.Low),
    #'Fiery Globe(EnemyFromBoss)':(currentType,              0x689,enemyMemoryUsage.Low),
    #'Icy Cube(EnemyFromBoss)':(currentType,                 0x68A,enemyMemoryUsage.Low),
    #'Magnum Loader W':(currentType,                        0x68B),
    #'Magnum Loader B':(currentType,                        0x6B5),
    # 'Magnum Loader Y':(currentType,                       0x6B6),
    # 'Magnum Loader G':(currentType,                       0x6B7),
    'Pirate A':(currentType,                               0x453),
    'Pirate B':(currentType,                               0x454),
    'Pirate C':(currentType,                               0x455),
    'Graveyard':(currentType,                               0x6EE,enemyMemoryUsage.High),
    'Graveyard (HW)':(currentType,                          0x6EF,enemyMemoryUsage.High),
    'Toy Soldier':(currentType,                             0x6F0,enemyMemoryUsage.High),
    'Toy Soldier(HW)':(currentType,                         0x6F1,enemyMemoryUsage.High),
    #'Bolt Tower + Rapid Thruster':(currentType,            0x71D),
    'Trick Ghost(EX)':(currentType,                         0x723),
    'Aeroplane(TR)':(currentType,                           0x724),
    'Minute Bomb(EX)':(currentType,                         0x725,enemyMemoryUsage.Low),
    'Hammer Frame(EX)':(currentType,                        0x726),
    'Hot Rod(EX)':(currentType,                             0x727,enemyMemoryUsage.High),
    'Cannon Gun(EX)':(currentType,                          0x728),
    'Driller Mole(EX)':(currentType,                        0x729,enemyMemoryUsage.Low),
    'Emerald Blues(EX)':(currentType,                       0x72A,enemyMemoryUsage.High),
    'Bookmaster (EX)':(currentType,                         0x72B,enemyMemoryUsage.High),
    'Neoshadow(EX)':(currentType,                           0x72C),
    'Creeper Plant(EX)':(currentType,                       0x72D,enemyMemoryUsage.High),
    'Soldier(HW)':(currentType,                             0x72E),
    'Soldier(EX)':(currentType,                             0x72F),
    'Shadow (TR)':(currentType,                             0x730,enemyMemoryUsage.Low),
    'Shadow (HW)':(currentType,                             0x731,enemyMemoryUsage.Low),
    'Shadow(TR2)':(currentType,                             0x732,enemyMemoryUsage.Low),
    'Rapid Thruster(TR)':(currentType,                      0x733,enemyMemoryUsage.Low),
    'Armored Knight(EX)':(currentType,                      0x735,enemyMemoryUsage.Low),
    'Surveillance Robot(EX)':(currentType,                  0x737),
    #'Soldier(TR)':(currentType,                             0x739),
    'Emerald Blues(Tron)':(currentType,                     0x73C,enemyMemoryUsage.High),
    #'Hook Bat (EX)':(currentType,                          0x75F),
    'Large Body(TR)':(currentType,                          0x7E9,enemyMemoryUsage.High),
    #'Scar’s Ghost':(currentType,                           0x833),
    'Bolt Tower(LOD)':(currentType,                         0x8BE,enemyMemoryUsage.Low),
    'Vivi (Clone)':(currentType,                            0x8D0,enemyMemoryUsage.Medium),
    'Magic Phantom':(currentType,                           0x963),
    'Beffudler':(currentType,                               0x964),
    'Iron Hammer':(currentType,                             0x965),
    'Mad Ride':(currentType,                                0x966),
    'Camo Cannon':(currentType,                             0x967),
    'Reckless':(currentType,                                0x968,enemyMemoryUsage.High),
    'Lance Warrior':(currentType,                           0x969),
    'Aerial Champ':(currentType,                            0x96A),
    'Necromancer':(currentType,                             0x96B,enemyMemoryUsage.High),
    'Spring Metal':(currentType,                            0x96C,enemyMemoryUsage.High),
    'Aerial Viking':(currentType,                           0x96D),
    'Runemaster':(currentType,                              0x96E,enemyMemoryUsage.High),
    'Bulky Vendor (EX)':(currentType,                       0x9CD),
    'Demyx\'s Water Clone (Data)':(currentType,             0x9FA,enemyMemoryUsage.Low),
}
currentType = enemyType.Boss
boss_table = { ### It's pointless to make multiple bosses for additional cups, so we will use weighted random bosses so that we dont end up seeing 50 of the same boss in a run.
    'Shan-Yu'                           :(currentType,                         0x015),
    #'Hades(FirstFight)'                 :(currentType,                         0x15E),
    'Cerberus'                          :(currentType,                         0x15F),
    #'Thresholder'                       :(currentType,                         0x161),
    'Dark Thorn'                        :(currentType,                         0x162),
    #'Shadow Stalker'                    :(currentType,                         0x163),
    'Scar'                              :(currentType,                         0x29C),
    'Volcanic Lord'                     :(currentType,                         0x40B),
    'Blizzard Lord'                     :(currentType,                         0x40C),
    #'Groundshaker'                      :(currentType,                         0x459),
    'Prison Keeper'                     :(currentType,                         0x5CE),
    'The Experiment'                    :(currentType,                         0x5D0),
    'Grim Reaper'                       :(currentType,                         0x607,enemyMemoryUsage.High),
    'Pete(Part2)'                       :(currentType,                         0x6BC),
    'Beast(Boss)'                       :(currentType,                         0x2ce),
    #'Shadow Roxas'                     :(currentType,                         0x754),
    'Hostile Program'                   :(currentType,                 0x4B8),
    #'Axel I'                            :(currentType,                         0x8B5),
    'Old Pete'                            :(currentType,                         0x647),
    'Hades(Cups)'                       :(currentType,                         0x90E),
    'Pete(ChampionFight)'               :(currentType,                         0x90F),
    'Hercules'                          :(currentType,                         0x910),
    #Org 13 Normal Boss Encounters
    'Marluxia'                          :(currentType,                         0x923,enemyMemoryUsage.High),
    'Vexen'                             :(currentType,                         0x933,enemyMemoryUsage.High),
    'Lexaeus'                           :(currentType,                         0x935,enemyMemoryUsage.High),
    'Roxas'                             :(currentType,                         0x951,enemyMemoryUsage.High),
    'Larxene'                           :(currentType,                         0x962,enemyMemoryUsage.High),
    'Zexion'                            :(currentType,                         0x97B,enemyMemoryUsage.High),
    'Axel II'                           :(currentType,                         0x051,enemyMemoryUsage.High),
    'Demyx'                             :(currentType,                         0x8F7,enemyMemoryUsage.High),
    'Saix'                              :(currentType,                         0x6C9,enemyMemoryUsage.High),
    'Xaldin'                            :(currentType,                         0x3E5,enemyMemoryUsage.High),
    'Xemnas'                            :(currentType,                         0x646,enemyMemoryUsage.High),
    'Luxord'                            :(currentType,                         0x5F8,enemyMemoryUsage.High),
    'Xigbar'                            :(currentType,                         0x622,enemyMemoryUsage.High),
    'Final Xemnas'                      :(currentType,                         0x81F,enemyMemoryUsage.High),
    'Armored Xemnas'                      :(currentType,                         0x85C,enemyMemoryUsage.High),
}
currentType = enemyType.SuperBoss
superBoss_table = {

    'Sephiroth'                         :(currentType,                         0x8B6),
    'Terra/Lingering Will'              :(currentType,                         0x96F),
    #Org 13 Data fights
    'Axel (Data)'                              :(currentType,                         0x9C4,enemyMemoryUsage.High), #unique
    'Xigbar (Data)'                            :(currentType,                         0x9C5,enemyMemoryUsage.High), #unique
    'Saix (Data)'                              :(currentType,                         0x9C6,enemyMemoryUsage.High), #unique
    'Luxord (Data)'                            :(currentType,                         0x9C8,enemyMemoryUsage.High), #unique
    'Xemnas (Data)'                            :(currentType,                         0x9C9,enemyMemoryUsage.High), #unique
    'Final Xemnas (Data)'                      :(currentType,                         0x9CA,enemyMemoryUsage.High), #unique
    'Xaldin (Data)'                            :(currentType,                         0x9CB,enemyMemoryUsage.High), #unique
    'Demyx (Data)'                             :(currentType,                         0x9CC,enemyMemoryUsage.High), #unique
    'Roxas (Data)'                             :(currentType,                         0x951,enemyMemoryUsage.High), #non unique?
    'Lexaeus(Data)'                            :(currentType,                         0x935,enemyMemoryUsage.High), #non unique?
    'Vexen (Data)'                             :(currentType,                         0x933,enemyMemoryUsage.High), #non unique?
    'Marluxia (Data)'                          :(currentType,                         0x923,enemyMemoryUsage.High), #non unique?
    'Larxene (Data)'                           :(currentType,                         0x962,enemyMemoryUsage.High), #non unique?
    'Zexion (Data)'                            :(currentType,                         0x97B,enemyMemoryUsage.High), #non unique?
}
currentType = enemyType.Ally
ally_table = {

    'Hercules (Ally)'                         :(currentType,                         0x16A),
    'Minnie (Ally)'                         :(currentType,                         0x4BB), #Blacklisted minnie spawns so she can spawn but still have her part unmodified
    'Axel (Ally)'                         :(currentType,                         0x4DC),
    'Timon (Ally)'                         :(currentType,                         0x551),
    'Pumbaa (Ally)'                         :(currentType,                         0x552),
    'Leon (Ally)'                         :(currentType,                         0x61C),
    'Cloud (Ally)'                         :(currentType,                         0x688),
    'Yuffie (Ally)'                         :(currentType,                         0x6B0),
    'Tifa (Ally)'                         :(currentType,                         0x6B3),
    'Eeyore (Ally)'                         :(currentType,                         0x6C2),
    'Tigger (Ally)'                         :(currentType,                         0x6C3),
    'Piglet (Ally)'                         :(currentType,                         0x6C4),
    'Roo (Ally)'                         :(currentType,                         0x6C5),
    'Mickey (Ally)'                         :(currentType,                         0x764),
}

blackListUniqueID_Enemy = {

    'TT':{
        14:{
            35, #blacklist invincible dusk
            39, #blacklist munny dusk
        },
        4:{
            56, #blacklist invincible dusk the next day
        },

    },
    'TR':{
        2:{
            #6, #blacklist light cycle enemyes
            #11, #blacklist light cycle enemyieirjaseofdshjfaijs
            #13, #blacklist light cycle enemyes
        },
    },
    'HB':{
        33:{6,18} #blacklist vexen leftover data. Probrably used before making his own arena
    },
    'HE':{
        8:{41}, #blacklist 2nd pete fight too low of memory
        9:{11} #Blacklist hercules ally from randomization
    },
    #'MU':{
        #2:{85,86,87,91,92,95,96},#????
    #},
    'DC':{
        0:{39}, #blacklist minnie ally data so its completeable
        1:{19}, #blacklist minnie ally data so its completeable
        2:{156,157,158}
    },
    'EH':{
        20:{5,10} #blacklist Final xemnas clones
    },
    'BB':{
        5:{20}, #blacklist dark thorn copy
        11:{60} #blacklist dark thorn copy
    },
    'NM':{
        7:{11}, #blacklist the experiment clone thingy
    },
    'CA':{
        18:{9}, #blacklist the clone of the grim reaper
    }

}
blackListGroup_Enemy = {
    'MU':{
        5:{'b_40'}, #Weird fight where things break A TON
     },
    'CA':{
        1:{'b_40'}, # Pirates losing fight & softlock loading in afterwards
     },
    #'HE':{
        #5:{'b_40'}, #black list hades escape, runs out of memory frequently
    #},
}
blackListUCM_List = [#0x150,# Destroyable Land Of Dragon objects
                     #0x14e,
                     #0x14f,
                     0x016,# Hayabusa Shan-Yu Fight
                     ] #These are ucms blacklisted/removed for improved memory performance

class UCMProperty:
    def __init__(self, code,type=enemyType.Normal,useEnemyInRandomEnemyGen=True,replaceEnemyInRandomization=True,extraEnemyData=-1,extraEnemyData2=-1,extraEnemyDataRandom=False,extraEnemyDataRange=None,PositionOffset=[0,0,0]):
        self.code = code
        self.type = type
        self.useEnemyInRandomEnemyGen = useEnemyInRandomEnemyGen
        self.replaceEnemyInRandomization = replaceEnemyInRandomization
        self.extraEnemyDataRandom= extraEnemyDataRandom
        self.extraEnemyDataRange= extraEnemyDataRange
        self.extraEnemyData = extraEnemyData
        self.extraEnemyData2 = extraEnemyData2
        self.positionOffset = PositionOffset #XYZ
        if self.extraEnemyDataRandom:
            self.extraEnemyData = random.choice(self.extraEnemyDataRange)
UCMProperties = { #Use this to set some properties of certain UCMS. (Use this enemy in random enemy generation, Use this enemy if we should replace it for randomization)
    #UCMProperty(0x8B5,enemyType.Boss,False,True),#Axel 1
    UCMProperty(0x647,enemyType.Boss,False,True),#Old Pete
    UCMProperty(0x6BC,enemyType.Boss,False,True),#Old Pete
    UCMProperty(0x90F,enemyType.Boss,False,True),#Old Pete
    UCMProperty(0x4B8,enemyType.Boss,False,True),#Hostile Program
    UCMProperty(0x453,enemyType.Normal,False,True),#Pirates A
    UCMProperty(0x454,enemyType.Normal,False,True),#B
    UCMProperty(0x455,enemyType.Normal,False,True),#C
    UCMProperty(0x607,enemyType.Boss,extraEnemyData=1,extraEnemyData2=0), #Grim reaper property to prevent invinciblity
    UCMProperty(0x2ce,enemyType.Boss,False,True), #Beast fight
    UCMProperty(0x8D0,enemyType.Normal,False,True), #Viviclone
    UCMProperty(0x00F,enemyType.Normal,extraEnemyDataRandom=True,extraEnemyDataRange=range(0,3)), #Living Bone random type of enemy
    UCMProperty(0x85C,enemyType.Boss,PositionOffset = [0,120,0]), #Armored Xemnas Position Y changing to move to the ground

    #Org 13 Normal Boss Properties
    UCMProperty(0x923,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x933,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x935,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x951,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x962,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x97B,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x051,enemyType.Boss,replaceEnemyInRandomization=False,extraEnemyData=0),
    UCMProperty(0x8F7,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x6C9,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x3E5,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x646,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x5F8,enemyType.Boss,extraEnemyData=0),
    UCMProperty(0x622,enemyType.Boss,extraEnemyData=0,extraEnemyData2=1),
    UCMProperty(0x81F,enemyType.Boss,extraEnemyData=1), #Xemnas will not appear otherwise
    #Org 13 Superboss Properties
    UCMProperty(0x9C4,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9C5,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9C6,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9C8,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9C9,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9CA,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9CB,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x9CC,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x951,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x935,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x933,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x923,enemyType.SuperBoss,extraEnemyData=1),
    UCMProperty(0x962,enemyType.SuperBoss,extraEnemyData=0,extraEnemyData2=1),
    UCMProperty(0x97B,enemyType.SuperBoss,extraEnemyData=1),
}
LuxordTimerBar =    ('EH14_MS103')
DemyxWaterCloneBar =('HB04_MS403') #1C Bonus level
SaixBeserkBar =     ('EH15_MS104')
SephirothBattle =   ('HB01_MS601')
LexPowerBar =       ('HB33_FM_LEX')
VexenAntiSoraBar =  ('HB32_FM_VEX')
ZexionBook =        ('HB34_FM_ZEX')
MarluxiaMSN =       ('HB38_FM_MAR')
LarxeneMSN =       ('HB33_FM_LAR')
#Xemnas1MSN =       ('EH19_MS105')

"""
might be better to: go to all ard files, find boss UCM in all of them, 
find what that UCM uses for its mission, then store it somehow and use it how we want to when we want to spawn any boss
but its much easier to just manually do it for those few instances where bosses need it
"""
bossMSNTable = {
        (0x933):VexenAntiSoraBar, #Data bar anti sora clone
        #(0x97B):'HE17_KINOKO_ZEX', kinoko== cutscene?
        (0x935):LexPowerBar, #Lex's power bar meter
        (0x97B):ZexionBook, #Zexion book stuff?
        (0x923):MarluxiaMSN, #Marluxia
        (0x9C8):LuxordTimerBar, #Luxord timer bar
        (0x5F8):LuxordTimerBar, #Luxord timer bar
        (0x9CC):DemyxWaterCloneBar, #Demyx Water clone bar
        (0x8F7):DemyxWaterCloneBar, #Demyx Water clone bar
        (0x9C6):SaixBeserkBar, #Saix beserk meter
        (0x6C9):SaixBeserkBar, #Saix beserk meter
        (0x8B6):SephirothBattle, #Sephiroth Battle
        (0x962):LarxeneMSN, #Larxene Battle
        #(0x9C9):Xemnas1MSN, #Xemnas Data Battle
        #(0x646):Xemnas1MSN, #Xemnas Normal Battle



}