import random
from enemyes import *


def generate_enemy(conf_level: dict, enemies, boss, kills_my_boss):
    while True:
        try:
            rand = random.choice(list(conf_level))
        except IndexError:
            return
        if conf_level[rand]:
            break
        else:
            del conf_level[rand]
            try:
                rand = random.choice(list(conf_level))
            except IndexError:
                return
    if rand == 'enemy_1':
        enemy = Enemy1()
        enemies.add(enemy)
        conf_level['enemy_1'] -= 1
    elif rand == 'enemy_2':
        enemy = Enemy2()
        enemies.add(enemy)
        conf_level['enemy_2'] -= 1

    elif rand == 'enemy_3':
        enemy = Enemy3()
        enemies.add(enemy)
        conf_level['enemy_3'] -= 1

    if not boss:
        if kills_my_boss >= 50:
            if rand == 'boss_1':
                enemy = Boss1()
                enemies.add(enemy)
                conf_level['boss_1'] -= 1
                boss = True
                kills_my_boss = 0

            elif rand == 'boss_2':
                enemy = Boss2()
                enemies.add(enemy)
                conf_level['boss_2'] -= 1
                boss = True
                kills_my_boss = 0

            elif rand == 'boss_3':
                enemy = Boss3()
                enemies.add(enemy)
                conf_level['boss_3'] -= 1
                boss = True
                kills_my_boss = 0

    return conf_level, enemies, boss, kills_my_boss
