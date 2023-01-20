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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                coords = pygame.mouse.get_pos()
                if coords[0] >= screen_width // 2:
                    level = Level(level_0, screen)
                else:
                    level = Level(level_1, screen)

                start = True

    if start:
        screen.fill('grey')
        if level.run():
            start = False
            CDR = WCDR
    else:
        screen.fill('black')
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('1', 1, (255, 255, 255))
        text2 = f1.render('2', 1, (255, 255, 255))
        if CDR > 0:
            text3 = f1.render('YOU WIN', 1, (255, 0, 0))
            screen.blit(text3, (screen_width // 2 - 20, screen_height // 2 - 40))
        screen.blit(text1, (screen_width // 2 - 20, screen_height // 2))
        screen.blit(text2, (screen_width // 2 + 20, screen_height // 2))

    pygame.display.update()
    clock.tick(60)
