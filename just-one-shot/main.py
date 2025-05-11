# ============ Import and Initialize ============
import random
import sys

import pygame

from config import *

pygame.init()
pygame.font.init()

# ============ SCREEN ============
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Just One Shot")

# ============ CLOCK ===========
clock = pygame.time.Clock()

# ============ FONT ============
font = pygame.font.Font(None, 32)


# ============ GAME LOOP ============
def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)
        pygame.display.flip()


main()
