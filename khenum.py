from enum import IntEnum

class AbilityClass(IntEnum):
    action = 0
    support = 1
class AbilityType(IntEnum):
    Normal = 0
    Additive = 1
class AbilityTypeGained(IntEnum):
    Normal = 0
    DriveForm = 1
    CriticalBonus = 2
class KHCharacter(IntEnum):
    Sora = 0
    Donald = 1
    Goofy = 2
class AbilityTable_enum(IntEnum):
    Action = 0
    Support = 1
    LevelUp = 2
class CharacterBoostType(IntEnum):
    HPBoosts = 0
    MPBoosts = 1
    ArmorSlots = 2
    DriveUpgrades = 3
    Items = 4
    Accessory = 5
class FormTypeEnum(IntEnum):
    Summon = 0
    Valor = 1
    Wisdom = 2
    Limit = 3
    Master = 4
    Final = 5
    Anti = 6
class enemyMemoryUsage(IntEnum):
    Low = 0
    Medium = 1
    High =2
class enemyType(IntEnum):
    Normal = 0
    Ally = 1
    Boss =2
    SuperBoss =3
    #AbilityItem = 6
    #AbilityItem2 = 7
class itemType(IntEnum):
    Item = 0
    Equipment = 1
    Armor =2
    Accessory =3
    Recipe =4
    KeyItem =5
    Synthesis =6
    Magic =7
    Drives =8
    Summons =9
    Maps =10
class EquipmentStats(IntEnum):
    StrengthStat = 0
    MagicStat = 1
    DefenseStat = 2
    APStat = 3
    PhysicalResist = 4 #For these 100 means you will take normal damage, going lower means you will resist damage and above is that you will take more damage
    FireResist = 5
    BlizzardResist = 6
    ThunderResist = 7
    DarkResist = 8
    LightResist = 9 #Sora's explosion for example
    GlobalResistance = 10 #Resistance to all effects
    DriveModifier = 11 #Shouldn't be used?
    #AbilityItem = 6
    #AbilityItem2 = 7