import pygame

import lvl_game
from enemyes import *
from config import *
import datetime
from endless_game import generate_enemy

FPS = 60

pygame.init()
pygame.font.init()

with open('settings.json') as f:
    settings = json.load(f)

PLAYER_HEALTH, PROKACHKA_HEALTH = settings['stats']['health'], 20
PLAYER_SPEED, PROKACHKA_SPEED = settings['stats']['speed'], 10
BULLET_SPEED, PROKACHKA_BULLET_SPEED = settings['stats']['bullet_speed'], 10
BULLET_DAMAGE, PROKACHKA_BULLET_DAMAGE = settings['stats']['bullet_damage'], 15
BULLET_COL, PROKACHKA_BULLET_COL = settings['stats']['bullet_col'], 10
CURRENT_LEVEL = settings['stats']['level']
ENABLE_SOUND = settings['stats']['enable_sound']

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Wars")
game_over_music = pygame.mixer.Sound('data/game_over.mp3')
shot_music = pygame.mixer.Sound('data/shot.mp3')
crash_music = pygame.mixer.Sound('data/crash.mp3')
victrel_music = pygame.mixer.Sound('data/vistrel.mp3')
win_music = pygame.mixer.Sound('data/win_music.mp3')


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


def screen_results():
    with open('results.csv') as csvfile:
        data = sorted([[line.split(',')[0], int(line.split(',')[1]), line.split(',')[2]] for line in
                       csvfile.read().split('\n')[1:]], key=lambda x: x[1], reverse=True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return

        font = pygame.font.SysFont('Arial', 20)
        text_up = font.render('Дата    Очки    Убийства', False, (255, 255, 255))
        screen.fill((0, 0, 0))
        fon = pygame.image.load('data/fon_start_screen.jpeg')
        fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        screen.blit(fon, (0, 0))
        screen.blit(text_up, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, 10))
        k = 10 + text_up.get_height()
        for res in data[:100]:
            text = font.render('    '.join([res[0].split()[0], str(res[1]), res[2]]), False, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, k))
            k += text.get_height()

        text_main_menu = font.render('Выйти в главное меню(Esc)', False, (255, 255, 255))
        screen.blit(text_main_menu, (10, SCREEN_HEIGHT - text_main_menu.get_height()))

        pygame.display.flip()


def screen_settings():
    global ENABLE_SOUND
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                with open('settings.json', mode='w') as f:
                    json.dump(settings, f)
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if ENABLE_SOUND == 'True':
                        ENABLE_SOUND = 'False'
                        settings['stats']['enable_sound'] = 'False'
                    else:
                        ENABLE_SOUND = 'True'
                        settings['stats']['enable_sound'] = 'True'
                if event.key == pygame.K_ESCAPE:
                    start_screen()
                    return
        fon = pygame.image.load('data/fon_start_screen.jpeg')
        fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        font = pygame.font.SysFont('Arial', 30)
        text_up = font.render('Настройки', False, (255, 255, 255))
        text_sound = font.render(f'Музыка: {"On" if ENABLE_SOUND == "True" else "Off"} (1)', False, (255, 255, 255))
        text_back = font.render('Назад', False, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(text_up, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, 10))
        screen.blit(text_sound, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT * 0.3))
        screen.blit(text_back, (30, SCREEN_HEIGHT - text_back.get_height() - 30))
        pygame.display.flip()


def shop_screen():
    global PLAYER_HEALTH, PLAYER_SPEED, BULLET_SPEED, BULLET_DAMAGE, BULLET_COL, settings
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('settings.json', mode='w') as f:
                    json.dump(settings, f)
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    with open('settings.json', mode='w') as f:
                        json.dump(settings, f)
                    start_screen()
                    return
                if event.key == pygame.K_1:
                    if settings['stats']['cash'] >= settings["shop"]["price_up_health"]:
                        print(1)
                        PLAYER_HEALTH = round(PLAYER_HEALTH * (PROKACHKA_HEALTH / 100 + 1), 2)
                        settings['stats']['health'] = PLAYER_HEALTH
                        settings['stats']['cash'] -= settings["shop"]["price_up_health"]
                        settings["shop"]["price_up_health"] = int(
                            round(settings["shop"]["price_up_health"] * (PROKACHKA_HEALTH / 100 + 1.3), 0))
                if event.key == pygame.K_2:
                    if settings['stats']['cash'] >= settings["shop"]["price_up_speed"]:
                        PLAYER_SPEED = round(PLAYER_SPEED * (PROKACHKA_SPEED / 100 + 1), 2)
                        settings['stats']['speed'] = PLAYER_SPEED
                        settings['stats']['cash'] -= settings["shop"]["price_up_speed"]
                        settings["shop"]["price_up_speed"] = int(
                            round(settings["shop"]["price_up_speed"] * (PROKACHKA_SPEED / 100 + 1.3), 0))
                if event.key == pygame.K_3:
                    if settings['stats']['cash'] >= settings["shop"]["price_up_bullet_speed"]:
                        BULLET_SPEED = round(BULLET_SPEED * (PROKACHKA_BULLET_SPEED / 100 + 1), 2)
                        settings['stats']['bullet_speed'] = BULLET_SPEED
                        settings['stats']['cash'] -= settings["shop"]["price_up_bullet_speed"]
                        settings["shop"]["price_up_bullet_speed"] = int(
                            round(settings["shop"]["price_up_bullet_speed"] * (PROKACHKA_BULLET_SPEED / 100 + 1.3), 0))
                if event.key == pygame.K_4:
                    if settings['stats']['cash'] >= settings["shop"]["price_up_bullet_damage"]:
                        BULLET_DAMAGE = round(BULLET_DAMAGE * (PROKACHKA_BULLET_DAMAGE / 100 + 1), 2)
                        settings['stats']['bullet_damage'] = BULLET_DAMAGE
                        settings['stats']['cash'] -= settings["shop"]["price_up_bullet_damage"]
                        settings["shop"]["price_up_bullet_damage"] = int(
                            round(settings["shop"]["price_up_bullet_damage"] * (PROKACHKA_BULLET_DAMAGE / 100 + 1.3),
                                  0))
                if event.key == pygame.K_5:
                    if settings['stats']['cash'] >= settings["shop"]["price_up_bullet_col"]:
                        BULLET_COL = (BULLET_COL * (PROKACHKA_BULLET_COL / 100 + 1)) // 1
                        settings['stats']['bullet_col'] = BULLET_COL
                        settings['stats']['cash'] -= settings["shop"]["price_up_bullet_col"]
                        settings["shop"]["price_up_bullet_col"] = int(
                            round(settings["shop"]["price_up_bullet_col"] * (PROKACHKA_BULLET_COL / 100 + 1.3), 0))

        fon = pygame.image.load('data/fon_start_screen.jpeg')
        fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        font = pygame.font.SysFont('Arial', 25)
        text_shop = font.render('Магазин', False, (255, 255, 255))
        text_up_health = font.render(
            f'(1) Увеличить здоровье: {PLAYER_HEALTH} + {PROKACHKA_HEALTH}%. '
            f'Цена: {settings["shop"]["price_up_health"]}',
            False,
            (0, 255, 0))
        text_up_speed = font.render(
            f'(2) Увеличить скорость передвижения: {PLAYER_SPEED} + {PROKACHKA_SPEED}%. '
            f'Цена: {settings["shop"]["price_up_speed"]}',
            False,
            (0, 255, 0))
        text_up_bullet_speed = font.render(
            f'(3) Увеличить скорость пуль: {BULLET_SPEED} + {PROKACHKA_BULLET_SPEED}% '
            f'Цена: {settings["shop"]["price_up_bullet_speed"]}',
            False,
            (0, 255, 0))
        text_up_bullet_damage = font.render(
            f'(4) Увеличить урон: {BULLET_DAMAGE} + {PROKACHKA_BULLET_DAMAGE}% '
            f'Цена: {settings["shop"]["price_up_bullet_damage"]}',
            False,
            (0, 255, 0))
        text_up_bullet_col = font.render(f'(5) Увеличить количество пуль, выпускаемых за раз: '
                                         f'{BULLET_COL} + {PROKACHKA_BULLET_COL}% '
                                         f'Цена: {settings["shop"]["price_up_bullet_col"]}',
                                         False, (0, 255, 0))
        balance_text = font.render(f"Ваш баланс: {settings['stats']['cash']}", False, (255, 255, 255))
        to_main_menu_text = font.render("(Esc) Выйти в главное меню", False, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(text_shop, (SCREEN_WIDTH // 2 - text_shop.get_width() // 2, 20))
        screen.blit(balance_text, (SCREEN_WIDTH - balance_text.get_width() - 20, 20))
        screen.blit(to_main_menu_text, (20, SCREEN_HEIGHT - 20 - to_main_menu_text.get_height()))
        screen.blit(text_up_health, (SCREEN_WIDTH // 2 - text_up_health.get_width() // 2, SCREEN_HEIGHT * 0.1))
        screen.blit(text_up_speed, (SCREEN_WIDTH // 2 - text_up_speed.get_width() // 2, SCREEN_HEIGHT * 0.3))
        screen.blit(text_up_bullet_speed,
                    (SCREEN_WIDTH // 2 - text_up_bullet_speed.get_width() // 2, SCREEN_HEIGHT * 0.5))
        screen.blit(text_up_bullet_damage,
                    (SCREEN_WIDTH // 2 - text_up_bullet_damage.get_width() // 2, SCREEN_HEIGHT * 0.7))
        screen.blit(text_up_bullet_col, (SCREEN_WIDTH // 2 - text_up_bullet_col.get_width() // 2, SCREEN_HEIGHT * 0.9))
        pygame.display.flip()


def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_endless_game()
                    return
                if event.key == pygame.K_TAB:
                    start_lvl_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_1:
                    screen_results()
                    return
                if event.key == pygame.K_2:
                    screen_settings()
                    return
                if event.key == pygame.K_3:
                    shop_screen()
                    return

        fon = pygame.image.load('data/fon_start_screen.jpeg')
        fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        font = pygame.font.SysFont('Arial', 50)
        text_up = font.render('Главное меню', False, (255, 255, 255))
        font = pygame.font.SysFont('Arial', 35)
        text_start_endless_game = font.render('Бесконечный режим(Enter)', False, (255, 255, 255))
        text_start_lvl_game = font.render('Режим с уровнями(TAB)', False, (255, 255, 255))
        text_check_results = font.render('Результаты игр(1)', False, (255, 255, 255))
        text_settings = font.render('Настройки(2)', False, (255, 255, 255))
        text_shop = font.render('Магазин улучшений(3)', False, (255, 255, 255))
        text_exit = font.render('Выйти из игры(ESC)', False, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(text_up, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (9 / 10) * SCREEN_HEIGHT))
        screen.blit(text_start_endless_game,
                    (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (8 / 10) * SCREEN_HEIGHT))
        screen.blit(text_start_lvl_game,
                    (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (7 / 10) * SCREEN_HEIGHT))
        screen.blit(text_check_results,
                    (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (6 / 10) * SCREEN_HEIGHT))
        screen.blit(text_settings,
                    (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (5 / 10) * SCREEN_HEIGHT))
        screen.blit(text_shop, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (4 / 10) * SCREEN_HEIGHT))
        screen.blit(text_exit, (SCREEN_WIDTH // 2 - text_up.get_width() // 2, SCREEN_HEIGHT - (3 / 10) * SCREEN_HEIGHT))

        pygame.display.flip()


def finish_lvl_screen(title: str, from_game, status_win: str):
    if ENABLE_SOUND == 'True':
        if status_win == 'lost':
            game_over_music.play()
        elif status_win == 'win':
            win_music.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if from_game == 'lvl':
                        start_lvl_game()
                    else:
                        start_endless_game()
                    return
                if event.key == pygame.K_1:
                    start_screen()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        fon = pygame.image.load('data/fon_start_screen.jpeg')
        fon = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        font = pygame.font.SysFont('Arial', 30)
        result_game = font.render(title, False, (255, 255, 255))
        font = pygame.font.SysFont('Arial', 20)
        replay = font.render('Продолжить игру(Enter)', False, (255, 255, 255))
        main_menu = font.render('Главное меню(1)', False, (255, 255, 255))
        exit_game = font.render('Выйти из игры(Esc)', False, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(result_game, (SCREEN_WIDTH // 2 - result_game.get_width() // 2, SCREEN_HEIGHT * 0.2))
        screen.blit(replay, (SCREEN_WIDTH // 2 - result_game.get_width() // 2, SCREEN_HEIGHT * 0.4))
        screen.blit(main_menu, (SCREEN_WIDTH // 2 - result_game.get_width() // 2, SCREEN_HEIGHT * 0.5))
        screen.blit(exit_game, (SCREEN_WIDTH // 2 - result_game.get_width() // 2, SCREEN_HEIGHT * 0.7))

        pygame.display.flip()


def start_endless_game():
    global FPS
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
    kills_mejdu_boss = 0
    freeze_flag = False
    font = pygame.font.SysFont('Arial', 30)
    cheat_mode = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings['stats']['cash'] += score
                with open('settings.json', mode='w') as f:
                    json.dump(settings, f)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not freeze_flag:
                    if len(bullets) < BULLET_COL:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        if ENABLE_SOUND == 'True':
                            victrel_music.play()

                if event.key == pygame.K_ESCAPE:
                    if freeze_flag:
                        running = False
                    else:
                        freeze_flag = True
                if event.key == pygame.K_RETURN and freeze_flag:
                    freeze_flag = False
                if event.key == pygame.K_9:
                    if cheat_mode:
                        cheat_mode = False
                        FPS = 60
                    else:
                        cheat_mode = True
                        FPS = 500
        font_1 = pygame.font.SysFont('Arial', 20)
        if freeze_flag:
            text_pause_game = font.render('Игра приостановлена.', False, (255, 255, 255))
            text_finish_game = font_1.render('Для выхода нажмите Escape', False, (255, 0, 0))
            text_continue_game = font_1.render('Для продолжения нажмите Enter', False, (0, 255, 0))
            screen.blit(text_pause_game, (SCREEN_WIDTH // 2 - text_pause_game.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - text_pause_game.get_height() // 2))
            screen.blit(text_finish_game, (20, SCREEN_HEIGHT - 20 - text_finish_game.get_height()))
            screen.blit(text_continue_game, (
                SCREEN_WIDTH - 20 - text_continue_game.get_width(),
                SCREEN_HEIGHT - 20 - text_continue_game.get_height()))
            pygame.display.flip()
            continue
        all_sprites.add(bullets_boss)
        all_sprites.update()
        try:
            for enemy in enemies:
                if enemy.update():
                    if not cheat_mode:
                        hp -= enemy.damage_crash
                    enemies.remove(enemy)
                    kills_mejdu_boss += 1
        except TypeError:
            pass

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
        enemies, boss, kills_mejdu_boss = generate_enemy(kills, lvl_boss, boss, enemies,
                                                         chance_boss,
                                                         kills_mejdu_boss)
        if boss:
            if cheat_mode:
                boss = False

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet, hit in hits.items():
            if not cheat_mode:
                hit[0].health -= BULLET_DAMAGE
            if hit[0].health <= 0:
                if hit[0].__class__.__name__ in ['Boss1', 'Boss2', 'Boss3']:
                    boss = False
                score += hit[0].reward
                hit[0].kill()
                kills += 1
                if ENABLE_SOUND == 'True':
                    crash_music.play()
                kills_mejdu_boss += 1
            else:
                if ENABLE_SOUND == 'True':
                    shot_music.play()

        crash_in_player = pygame.sprite.spritecollide(player, enemies, True)
        for crash in crash_in_player:
            if not cheat_mode:
                hp -= crash.damage_crash
        if hp <= 0:
            running = False

        hits_boos_in_player = pygame.sprite.spritecollide(player, bullets_boss, True)
        for bul in hits_boos_in_player:
            if not cheat_mode:
                hp -= bul.damage
        if hp <= 0:
            running = False
            if ENABLE_SOUND == 'True':
                crash_music.play()

        hp_text = font_1.render(f'Ваше здоровье: {hp}', False, (255, 255, 255))
        score_text = font_1.render(f'Набранные очки: {score}', False, (255, 255, 255))

        bullets.update()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        enemies.draw(screen)
        screen.blit(hp_text, (10, 20))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width(), 20))

        pygame.display.flip()
        clock.tick(FPS)

    settings['stats']['cash'] += score
    with open('settings.json', mode='w') as f:
        json.dump(settings, f)
    with open('results.csv', mode='a') as csvfile:
        csvfile.write(f'\n{str(datetime.datetime.now())},{score},{kills}')
    all_sprites.clear(screen, screen)
    enemies.clear(screen, screen)
    bullets.clear(screen, screen)
    bullets.update()
    bullets.draw(screen)
    finish_lvl_screen(f'Набранные очки: {score}', 'endless', 'lost')
    pygame.quit()


def start_lvl_game():
    global CURRENT_LEVEL, FPS
    with open('levels.json') as f:
        CONF_LEVEL = json.load(f)[str(CURRENT_LEVEL)]
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
    running = True
    boss = False
    kills_my_boss = 0
    freeze_flag = False
    font = pygame.font.SysFont('Arial', 30)
    cheat_mode = False
    while running:
        if len(list(CONF_LEVEL)) == 0 and not boss:
            with open('settings.json', mode='w') as f:
                CURRENT_LEVEL = str(int(settings['stats']['level']) + 1) if int(
                    settings['stats']['level']) + 1 <= 4 else '4'
                settings['stats']['level'] = CURRENT_LEVEL
                json.dump(settings, f)
            with open('results.csv', mode='a') as csvfile:
                csvfile.write(f'\n{str(datetime.datetime.now())},{score},{kills}')
            all_sprites.clear(screen, screen)
            enemies.clear(screen, screen)
            bullets.clear(screen, screen)
            bullets.update()
            bullets.draw(screen)
            finish_lvl_screen(f'Вы победили! Ваши очки: {score}', 'lvl', 'win')
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings['stats']['cash'] += score
                with open('settings.json', mode='w') as f:
                    json.dump(settings, f)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not freeze_flag:
                    if len(bullets) < BULLET_COL:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        if ENABLE_SOUND == 'True':
                            victrel_music.play()
                if event.key == pygame.K_ESCAPE:
                    if freeze_flag:
                        running = False
                    else:
                        freeze_flag = True
                if event.key == pygame.K_RETURN:
                    freeze_flag = False
                if event.key == pygame.K_9:
                    if cheat_mode:
                        cheat_mode = False
                        FPS = 60
                    else:
                        cheat_mode = True
                        FPS = 500
        font_1 = pygame.font.SysFont('Arial', 20)
        if freeze_flag:
            text_pause_game = font.render('Игра приостановлена.', False, (255, 255, 255))
            text_finish_game = font_1.render('Для выхода нажмите Escape', False, (255, 0, 0))
            text_continue_game = font_1.render('Для продолжения нажмите Enter', False, (0, 255, 0))
            screen.blit(text_pause_game, (SCREEN_WIDTH // 2 - text_pause_game.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - text_pause_game.get_height() // 2))
            screen.blit(text_finish_game, (20, SCREEN_HEIGHT - 20 - text_finish_game.get_height()))
            screen.blit(text_continue_game, (
                SCREEN_WIDTH - 20 - text_continue_game.get_width(),
                SCREEN_HEIGHT - 20 - text_continue_game.get_height()))
            pygame.display.flip()
            continue

        all_sprites.add(bullets_boss)
        all_sprites.update()
        try:
            for enemy in enemies:
                if enemy.update():
                    if not cheat_mode:
                        hp -= enemy.damage_crash
                    enemies.remove(enemy)
                    kills_my_boss += 1
        except TypeError:
            pass

        if random.randint(1, 30) == 15:
            try:
                CONF_LEVEL, enemies, boss, kills_my_boss = lvl_game.generate_enemy(CONF_LEVEL, enemies, boss,
                                                                                   kills_my_boss)
            except TypeError:
                pass
        if boss:
            if cheat_mode:
                boss = False
        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet, hit in hits.items():
            if not cheat_mode:
                hit[0].health -= BULLET_DAMAGE
            if hit[0].health <= 0:
                if hit[0].__class__.__name__ in ['Boss1', 'Boss2', 'Boss3']:
                    boss = False
                score += hit[0].reward
                hit[0].kill()
                kills += 1
                if ENABLE_SOUND == 'True':
                    crash_music.play()
                kills_my_boss += 1
            else:
                if ENABLE_SOUND == 'True':
                    shot_music.play()

        crash_in_player = pygame.sprite.spritecollide(player, enemies, True)
        for crash in crash_in_player:
            if not cheat_mode:
                hp -= crash.damage_crash
            kills_my_boss += 1
        if hp <= 0:
            running = False

        hits_boos_in_player = pygame.sprite.spritecollide(player, bullets_boss, True)
        for bul in hits_boos_in_player:
            if not cheat_mode:
                hp -= bul.damage
        if hp <= 0:
            running = False
            if ENABLE_SOUND == 'True':
                crash_music.play()

        hp_text = font_1.render(f'Ваше здоровье: {hp}', False, (255, 255, 255))
        score_text = font_1.render(f'Набранные очки: {score}', False, (255, 255, 255))
        cur_level_text = font_1.render(f'Уровень: {str(CURRENT_LEVEL)}', False, (255, 255, 255))

        bullets.update()

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        enemies.draw(screen)
        all_sprites.draw(screen)

        screen.blit(hp_text, (10, 20))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width(), 20))
        screen.blit(cur_level_text, (SCREEN_WIDTH // 2 - cur_level_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    settings['stats']['cash'] += score
    with open('settings.json', mode='w') as f:
        json.dump(settings, f)
    with open('results.csv', mode='a') as csvfile:
        csvfile.write(f'\n{str(datetime.datetime.now())},{score},{kills}')
    all_sprites.clear(screen, screen)
    enemies.clear(screen, screen)
    bullets.clear(screen, screen)
    bullets.update()
    bullets.draw(screen)
    finish_lvl_screen(f'Вы проиграли. Набранные очки: {score}', 'lvl', 'lost')
    pygame.quit()
    return


if __name__ == "__main__":
    start_screen()
