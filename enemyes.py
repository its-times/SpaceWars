import pygame
import random

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 1000

class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy1.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy2.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 2.3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/enemy3.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 2.5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Дать возможность стрелять для Боссов и переработать их движение(чтобы двигались по горизонтали и меньше по вертикали)
class Boss1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss1.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Boss2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss2.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 3.3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Boss3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('data/boss3.png')
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), 0))
        self.speed = 3.5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()