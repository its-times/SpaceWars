import random
from enemyes import *

def generate_enemy(kills, lvl_boss, boss, enemies, all_sprites, chance_boss, kills_mejdu_boss):
    conf_spawn = [[0, 70], [70, 95], [95, 100]]
    conf_spawn = [[conf_spawn[0][0], int(round(conf_spawn[0][1] * (1 - (kills / 1000)), 0))],
                  [int(round(conf_spawn[1][0] * (1 - (kills / 1000)), 0)),
                   int(round(conf_spawn[1][1] * (1 - (kills / 1000)), 0))],
                  [int(round(conf_spawn[2][0] * (1 - (kills / 1000)), 0)),
                   int(round(conf_spawn[2][1] * (1 - (kills / 1000)), 0))]]


    if not boss:
        rand = random.randint(0, 101)
        if random.randint(1, 30) == 10:
            if conf_spawn[0][0] <= rand <= conf_spawn[0][1]:
                enemy = Enemy1()
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif conf_spawn[1][0] <= rand <= conf_spawn[1][1]:
                enemy = Enemy2()
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif conf_spawn[2][0] <= rand <= conf_spawn[2][1]:
                enemy = Enemy3()
                enemies.add(enemy)
                all_sprites.add(enemy)

    if not boss:
        if random.randint(1, 101) < chance_boss and kills_mejdu_boss >= 50:
            boss = True
            if lvl_boss == 1:
                boss_enemy = Boss1()
            elif lvl_boss == 2:
                boss_enemy = Boss2()
            else:
                boss_enemy = Boss3()
            enemies.add(boss_enemy)
            all_sprites.add(boss_enemy)
            kills_mejdu_boss = 0
    return enemies, all_sprites, boss, kills_mejdu_boss