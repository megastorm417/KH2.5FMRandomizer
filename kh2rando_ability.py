from kh2rando_abilityTable import Ability_Table
from khenum import AbilityTable_enum,AbilityType,AbilityTypeGained

class KHActionAbility:

    def __init__(self, name='', character = '', code=None,maximum=1,abilitytype=AbilityType.Normal,abilityLearned= AbilityTypeGained.Normal):
        self.name = name
        self.character = character
        self.code = code
        self.maximum = maximum
        self.abilityLearned = abilityLearned
        self.abilitytype = abilitytype



    def subtractQOne(self):
        if self.maximum > 0:
            self.maximum -= 1

    def emptyItem(self):
        return (self.maximum > 0 or self.maximum == -1)


    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name

class KHSLAbility:

    def __init__(self, name='', character = '', code=None,maximum = 1,abilitytype=AbilityType.Normal,abilityLearned= AbilityTypeGained.Normal):
        self.name = name
        self.character = character
        self.code = code
        self.maximum = maximum
        self.abilityLearned = abilityLearned
        self.abilitytype = abilitytype



    def subtractQOne(self):
        if self.maximum > 0:
            self.maximum -= 1

    def emptyItem(self):
        return (self.maximum > 0 or self.maximum == -1)


    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


def NewAbilityList():
    AbilityList = [[] for i in range(3)]

    def createItemsFromTable(table):
        for type in table:
            for item in table[type]:
                if item in table[type]:
                    if(type == AbilityTable_enum.Action):
                        new_item = KHActionAbility(item, *table[type][item])
                    elif type in (AbilityTable_enum.Support, AbilityTable_enum.LevelUp):
                        new_item = KHSLAbility(item, *table[type][item])
                    AbilityList[type].append(new_item)

    createItemsFromTable(Ability_Table)
    return AbilityList

