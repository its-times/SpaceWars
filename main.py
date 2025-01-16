import json

import pygame

from enemyes import *

pygame.init()

with open('settings.json') as f:
    settings = json.load(f)

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000
PLAYER_HEALTH = settings['health']
PLAYER_SPEED = settings['speed']
BULLET_SPEED = settings['bullet_speed']
BULLET_DAMAGE = settings['bullet_damage']
BULLET_COL = settings['bullet_col']

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Wars")

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
    clock = pygame.time.Clock()
    player = Player()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    all_sprites.add(player)

    score = 0
    hp = PLAYER_HEALTH

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if len(bullets) < BULLET_COL:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet )

        all_sprites.update()

        if random.randint(1, 30) == 1: # Заменить на систему выбора врагов исходя из уровня сложности/количества очков
            enemy = Enemy1()
            enemies.add(enemy)
            all_sprites.add(enemy)

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        score += len(hits) * 15

        crash_in_player = pygame.sprite.spritecollide(player, enemies, True)
        if len(crash_in_player) * 20 < hp:
            hp -= len(crash_in_player) * 20
        else:
            hp = 0
            running = False



        bullets.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)


    settings['cash'] += score
    with open('settings.json', mode='w') as f:
        json.dump(settings, f)
    pygame.quit()


if __name__ == "__main__":
    main()
