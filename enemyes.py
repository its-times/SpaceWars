import pygame
import random
import json
with open('settings.json') as f:
    settings = json.load(f)
HEALTH_PLAYER = settings['health']

from config import *

bullets_boss = pygame.sprite.Group()

class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy1.png')
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 250), 0))
        self.speed = 2
        self.damage_crash = HEALTH_PLAYER // 6
        self.reward = 20
        self.health = 20

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            return True
        return False



class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy2.png')
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 250), 0))
        self.speed = 2.3
        self.damage_crash = HEALTH_PLAYER // 4
        self.reward = 30
        self.health = 40

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            return True
        if random.randint(1, 15) == 2:
            rand = random.randint(1, 2)
            if rand == 1 and self.rect.x - self.speed * 2.5 >= 0:
                self.rect.x -= self.speed * 2.5
            elif rand == 2 and self.rect.x + self.rect.width + self.speed * 3 <= SCREEN_WIDTH:
                self.rect.x += self.speed * 2.5
            return False



class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy3.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 2.5
        self.damage_crash = HEALTH_PLAYER // 2
        self.reward = 40
        self.health = 60

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            return True
        rand = random.randint(1, 2)
        if rand == 1 and self.rect.x - self.speed * 3 >= 0:
            self.rect.x -= self.speed * 3
        elif rand == 2 and self.rect.x + self.rect.width + self.speed * 5 < SCREEN_WIDTH:
            self.rect.x += self.speed * 3
        return False


class Boss1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss1.png')
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 250), 0))
        self.speed = 3
        self.bullet_speed = 2
        self.flag = False
        self.damage_crash = HEALTH_PLAYER
        self.damage_bullet = 20
        self.reward = 100
        self.health = 100

    def update(self):
        global bullets_boss
        self.rect.y += self.speed * 0.2
        if self.rect.top > SCREEN_HEIGHT:
            return True
        if not self.flag:
            if self.rect.x - self.speed >= 0:
                self.rect.x -= self.speed
            else:
                self.flag = True
        else:
            if self.rect.x + self.rect.width + self.speed <= SCREEN_WIDTH:
                self.rect.x += self.speed
            else:
                self.flag = False
        rand = random.randint(1, 100)
        if rand == 5:
            bullet = BulletBoss(self.rect.centerx, self.rect.bottom, self.bullet_speed, self.damage_bullet)
            bullets_boss.add(bullet)
        return False



class Boss2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss2.png')
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 250), 0))
        self.speed = 3.3
        self.bullet_speed = 4
        self.flag = False
        self.damage_crash = HEALTH_PLAYER
        self.damage_bullet = 30
        self.reward = 150
        self.health = 140

    def update(self):
        global bullets_boss
        self.rect.y += self.speed * 0.4
        if self.rect.top > SCREEN_HEIGHT:
            return True
        if not self.flag:
            if self.rect.x - self.speed >= 0:
                self.rect.x -= self.speed
            else:
                self.flag = True
        else:
            if self.rect.x + self.rect.width + self.speed <= SCREEN_WIDTH:
                self.rect.x += self.speed
            else:
                self.flag = False
        rand = random.randint(1, 100)
        if rand == 5:
            bullet = BulletBoss(self.rect.centerx, self.rect.bottom, self.bullet_speed, self.damage_bullet)
            bullets_boss.add(bullet)
        return False


class Boss3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss3.png')
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 250), 0))
        self.speed = 3.5
        self.bullet_speed = 6
        self.flag = False
        self.damage_crash = HEALTH_PLAYER
        self.damage_bullet = 40
        self.reward = 200
        self.health = 180

    def update(self):
        global bullets_boss
        self.rect.y += self.speed * 0.5
        if self.rect.top > SCREEN_HEIGHT:
            return True
        if not self.flag:
            if self.rect.x - self.speed >= 0:
                self.rect.x -= self.speed
            else:
                self.flag = True
        else:
            if self.rect.x + self.rect.width + self.speed <= SCREEN_WIDTH:
                self.rect.x += self.speed
            else:
                self.flag = False
        rand = random.randint(1, 100)
        if rand == 5:
            bullet = BulletBoss(self.rect.centerx, self.rect.bottom, self.bullet_speed, self.damage_bullet)
            bullets_boss.add(bullet)
        return False


class BulletBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_speed, damage):
        super().__init__()
        self.image = pygame.image.load('data/bullet_enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.bullet_speed = bullet_speed
        self.damage = damage

    def update(self):
        self.rect.y += self.bullet_speed
        if self.rect.bottom > SCREEN_HEIGHT:
            return True