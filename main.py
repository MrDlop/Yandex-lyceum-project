import os

import pygame
import sys
from settings import *
from level import Level
from game_data import level_0, level_1

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen)
start = False
coins = 0
CDR = 0
WCDR = 10
WIN_CDR = 0


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


CDR_start = 2 * FPS

PREVIEW = pygame.image.load('graphics/start_image.PNG')
PREVIEW_RECT = PREVIEW.get_rect(center=(640, 360))

LOADING_BG = load_image("graphics/progress_bar/Loading_bar_background.png")
LOADING_BG_RECT = LOADING_BG.get_rect(center=(640, 560))

loading_bar = pygame.image.load("graphics/progress_bar/Loading_bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(340, 560))
loading_finished = False
loading_progress = 0
loading_bar_width = 8

WORK = CDR_start

restart = load_image("graphics/progress_bar/restart.png")
restart_rect = LOADING_BG.get_rect(center=(640, 350))

exit_ = load_image("graphics/progress_bar/exit.png")
exit_rect = LOADING_BG.get_rect(center=(800, 345))

cur_level = level_0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if CDR:
                coords = pygame.mouse.get_pos()
                if 710 >= coords[0] >= 630 and 405 >= coords[1] >= 320:
                    CDR = 0
                elif 550 >= coords[0] >= 460 and 405 >= coords[1] >= 320:
                    CDR = 0
                    level = Level(cur_level, screen)
                    CDR_start = WORK
                    start = True
            elif not start and CDR_start <= 0:
                coords = pygame.mouse.get_pos()
                if coords[0] >= screen_width // 2:
                    cur_level = level_0
                else:
                    cur_level = level_1

                level = Level(cur_level, screen)
                CDR_start = WORK
                start = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                CDR = 0
                CDR_start = WORK
                start = False
    if CDR:
        screen.fill((151, 159, 191))
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('YOU WIN', 1, (255, 0, 0))
        screen.blit(text1, (550, 200))
        screen.blit(restart, restart_rect)
        screen.blit(exit_, exit_rect)
        CDR_start = WORK
    elif CDR_start > 0:
        screen.fill((151, 159, 191))
        d = (WORK - CDR_start + 1) * 3
        loading_bar = pygame.transform.scale(loading_bar, (d, 69))
        loading_bar_rect = loading_bar.get_rect(midleft=(463, 560))
        screen.blit(PREVIEW, PREVIEW_RECT)
        screen.blit(LOADING_BG, LOADING_BG_RECT)
        screen.blit(loading_bar, loading_bar_rect)
        CDR_start -= 1
    elif start:
        screen.fill('grey')
        if level.run():
            start = False
            CDR = WCDR
    else:
        screen.fill((151, 159, 191))
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('1', 1, (255, 255, 255))
        text2 = f1.render('2', 1, (255, 255, 255))
        screen.blit(text1, (screen_width // 2 - 20, screen_height // 2))
        screen.blit(text2, (screen_width // 2 + 20, screen_height // 2))

    if pygame.display.update() == 1:
        WIN_CDR = 10
    clock.tick(FPS)
