import json
import random

import pygame

import endless_game
from enemyes import *
from config import *

pygame.init()

with open('settings.json') as f:
    settings = json.load(f)

PLAYER_HEALTH = settings['health']
PLAYER_SPEED = settings['speed']
BULLET_SPEED = settings['bullet_speed']
BULLET_DAMAGE = settings['bullet_damage']
BULLET_COL = settings['bullet_col']


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Wars")
game_over_music = pygame.mixer.Sound('data/game_over.mp3')
shot_music = pygame.mixer.Sound('data/shot.mp3')
crash_music = pygame.mixer.Sound('data/crash.mp3')
victrel_music = pygame.mixer.Sound('data/vistrel.mp3')

# Дописать систему выхода с экрана(отнимается хп)
# Сделать стартовый экран с началом игры(выбор режима), магазином прокачки и таблицей лидеров
# После боя записывать результат в csv файл, а также сохранять настройки игрока(после покупки новые улучшения)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/player.png')
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('data/bullet_player.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


def main():
    fon = pygame.image.load('data/fon.png')
    fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    clock = pygame.time.Clock()
    player = Player()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all_sprites.add(player)

    score = 0
    hp = PLAYER_HEALTH
    kills = 0
    conf_spawn = [[0, 70], [70, 95], [95, 100]]
    running = True
    boss = False
    lvl_boss = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings['cash'] += score
                with open('settings.json', mode='w') as f:
                    json.dump(settings, f)
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(bullets) < BULLET_COL:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    victrel_music. play()
        all_sprites.add(bullets_boss)
        all_sprites.update()

        conf_spawn = [[conf_spawn[0][0], int(round(conf_spawn[0][1] * (1 - (kills / 1000)), 0))],
                      [int(round(conf_spawn[1][0] * (1 - (kills / 1000)), 0)),
                      int(round(conf_spawn[1][1] * (1 - (kills / 1000)), 0))],
                      [int(round(conf_spawn[2][0] * (1 - (kills / 1000)), 0)),
                       int(round(conf_spawn[2][1] * (1 - (kills / 1000)), 0))]]

        chance_boss = kills / 50
        if chance_boss >= 100:
            if lvl_boss < 3:
                lvl_boss += 1
                chance_boss = 0
            else:
                chance_boss = chance_boss / 4
        kills_mejdu_boss = 0
        enemies, all_sprites, boss, kills_mejdu_boss = endless_game.generate_enemy(kills, lvl_boss, boss, enemies, all_sprites, chance_boss, kills_mejdu_boss)

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False )
        for bullet, hit in hits.items():
            hit[0].health -= BULLET_DAMAGE
            if hit[0].health <= 0:
                if hit[0].__class__.__name__ in ['Boss1', 'Boss2', 'Boss3']:
                    boss = False
                score += hit[0].reward
                hit[0].kill()
                kills += 1
                crash_music.play()
                kills_mejdu_boss += 1
            else:
                shot_music.play()

        crash_in_player = pygame.sprite.spritecollide(player, enemies, True)
        for crash in crash_in_player:
            hp -= crash.damage_crash
        if hp <= 0:
            running = False

        hits_boos_in_player = pygame.sprite.spritecollide(player, bullets_boss, True)
        for bul in hits_boos_in_player:
            hp -= bul.damage
        if hp <= 0:
            running = False
            crash_music.play()


        bullets.update()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    settings['cash'] += score
    with open('settings.json', mode='w') as f:
        json.dump(settings, f)

    pygame.quit()


if __name__ == "__main__":
    main()
