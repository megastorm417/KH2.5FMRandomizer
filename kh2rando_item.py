from kh2rando_itemTable import item_table, soraEquipment_table, donaldEquipment_table, goofyEquipment_table, armor_table, accessory_table, recipe_table, keyitem_table, synthesis_table, magic_table, drive_table, summon_table, maps_table
class KHItem:

    def __init__(self, name='', priority=False,essential = False, type=None, code=None,maximum=-1,agrabahRequirement=False,shopPrice=-1):
        self.name = name
        self.priority = priority
        self.essential = essential
        self.type = type
        self.code = code
        self.maximum = maximum
        self.agrabahRequirement= agrabahRequirement
        self.shopPrice = shopPrice #-1 shop price means it will use orginal

    #def copy(self):
        #return Item(self.name, self.priority, self.type, self.code, self.maximum,self.agrabahRequirement)
    
    def subtractQuantity(self,quan):
        if self.maximum > 0:
            self.maximum -= quan
    def subtractQOne(self):
        if self.maximum > 0:
            self.maximum -= 1

    def emptyItem(self):
        if(self.maximum > 0 or self.maximum == -1):
            return True
        else:
            return False

    def priority(self):
        return self.priority

    def essential(self):
        return self.essential
    def agrabahRequired(self):
        return self.agrabahRequirement
    def codeReturn(self):
        return self.code

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name
    
    
def NewItemList():
    ItemList = []
    def createItemsFromTable(table):
        for item in table:
            if item in table:
                new_item = KHItem(item,*table[item])
                ItemList.append(new_item)
                
    createItemsFromTable(item_table)
    createItemsFromTable(soraEquipment_table)
    createItemsFromTable(donaldEquipment_table)
    createItemsFromTable(goofyEquipment_table)
    createItemsFromTable(armor_table)
    createItemsFromTable(accessory_table)
    createItemsFromTable(recipe_table)
    createItemsFromTable(keyitem_table)
    createItemsFromTable(synthesis_table)
    createItemsFromTable(magic_table)
    createItemsFromTable(drive_table)
    createItemsFromTable(summon_table)
    createItemsFromTable(maps_table)
    return ItemList
def Generic_ItemList(): #Get most of items but not all
    ItemList = []
    def createItemsFromTable(table):
        for item in table:
            if item in table:
                new_item = KHItem(item,*table[item])
                ItemList.append(new_item)

    createItemsFromTable(item_table)
    createItemsFromTable(donaldEquipment_table)
    createItemsFromTable(goofyEquipment_table)
    createItemsFromTable(armor_table)
    createItemsFromTable(accessory_table)
    createItemsFromTable(synthesis_table)
    return ItemList
    