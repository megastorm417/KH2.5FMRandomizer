from kh2rando_enemyTable import enemy_table,boss_table,superBoss_table,ally_table
from khenum import enemyMemoryUsage
class KHucmObject:

    def __init__(self, name='', type= "Enemy", code = None,memoryUsage=enemyMemoryUsage.Medium):
        self.name = name
        self.type = type
        self.code = code
        self.memoryUsage = memoryUsage


def NewEnemyList():
    EnemyList = []
    def createEnemyFromTable(table):
        for enemy in table:
            if enemy in table:
                new_enemy = KHucmObject(enemy, *table[enemy])
                EnemyList.append(new_enemy)
                
    createEnemyFromTable(enemy_table)
    return EnemyList

def NewBossList():
    BossList = []
    def createEnemyFromTable(table):
        for enemy in table:
            if enemy in table:
                new_enemy = KHucmObject(enemy, *table[enemy])
                BossList.append(new_enemy)
                
    createEnemyFromTable(boss_table)
    return BossList

def NewSuperBossList():
    SuperBossList = []
    def createEnemyFromTable(table):
        for enemy in table:
            if enemy in table:
                new_enemy = KHucmObject(enemy, *table[enemy])
                SuperBossList.append(new_enemy)
                
    createEnemyFromTable(superBoss_table)
    return SuperBossList
def NewAllyList():
    AllyList = []
    def createEnemyFromTable(table):
        for enemy in table:
            if enemy in table:
                new_enemy = KHucmObject(enemy, *table[enemy])
                AllyList.append(new_enemy)

    createEnemyFromTable(ally_table)
    return AllyList