import pygame
import sys
from settings import *
from level import Level
from game_data import level_0

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)
start = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start = True

    if start:
        screen.fill('grey')
        level.run()
    else:
        screen.fill('black')
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('Start', 1, (255, 255, 255))
        screen.blit(text1, (screen_width // 2, screen_height // 2))

    pygame.display.update()
    clock.tick(60)
