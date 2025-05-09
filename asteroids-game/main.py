import json
import os
import sys

import pygame

# import Asteroid object from asteroid.py
from asteroid import Asteroid
from asteroidfield import AsteroidField

# import everything from the constants.py file
from constants import *

# import Player object from player.py
from player import Player
from shot import Shot

pygame.init()
pygame.font.init()

font = pygame.font.Font("freesansbold.ttf", 20)


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
        return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump({"high_score": score}, f)


def main():
    pygame.init()  # initialize the pygame module

    # screen function creates a GUI window and sets it to the constants passed in
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # create a clock object to control FPS
    clock = pygame.time.Clock()

    # create groups for screen management
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # instantiate Player object
    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    # set current delta time at 0
    dt = 0

    # set color hex code numbers
    black = 0, 0, 0

    # create score and game_over variables
    score = 0
    high_score = load_high_score()
    game_over = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if not game_over:
            updatable.update(dt)

            for a in asteroids:
                if a.collides_with(player):
                    game_over = True

                for shot in shots:
                    if a.collides_with(shot):
                        a.split()
                        score += 5

        screen.fill(black)

        for d in drawable:
            d.draw(screen)

        text = font.render("Score {0}".format(score), True, "white")
        screen.blit(text, (5, 10))

        high_score_text = font.render(
            "High Score {0}".format(high_score), True, "white"
        )
        screen.blit(high_score_text, (5, 35))

        # Game over logic
        if game_over:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_text = font.render(
                "Game Over! Press R to Restart or Q to Quit", True, "white"
            )
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 225, SCREEN_HEIGHT // 2))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
                return
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

        # limit FPS to 60
        dt = clock.tick(60) / 1000

        pygame.display.update()


if __name__ == "__main__":
    main()
