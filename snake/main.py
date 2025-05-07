import random
import sys

import pygame

pygame.init()
pygame.font.init()

# ========== Game Variables ==========

# Colors
black = 0, 0, 0
red = 255, 0, 0
purple = 255, 0, 255
green = 10, 255, 10
grey1 = 125, 125, 125
grey2 = 175, 175, 175

# Sizes
WIDTH = 480
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Move Coordinates
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

font = pygame.font.Font("freesansbold.ttf", 20)

# ========== Game Classes ==========


class Snake(object):
    def __init__(self):
        self.length = 1
        self.position = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = green

    def get_head_position(self):
        return self.position[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        new = (
            ((current[0] + (x * GRID_SIZE)) % WIDTH),
            (current[1] + (y * GRID_SIZE)) % HEIGHT,
        )
        self.position.insert(0, new)
        if len(self.position) > self.length:
            self.position.pop()

        # Return True if there was a collision
        return len(self.position) > 2 and new in self.position[2:]

    def reset(self):
        self.length = 1
        self.position = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for pos in self.position:
            r = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, black, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    return "quit"
        return None


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.random_pos()

    def random_pos(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        r = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, black, r, 1)


def draw_grid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if ((x + y) % 2) == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, grey1, r)
            else:
                rr = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, grey2, rr)


# ========== Main Game Logic ==========


def main():
    # Initialize Game
    pygame.init()
    pygame.font.init()

    # Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption("Snake Game")

    # Surface
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    # Clock
    clock = pygame.time.Clock()

    # Create Game Objects
    snake = Snake()
    food = Food()
    game_over = False
    score = 0

    # Game Loop
    while True:
        clock.tick(10)
        key_response = snake.handle_keys()

        # Restart Logic
        if game_over and key_response == "restart":
            snake = Snake()
            food = Food()
            score = 0
            game_over = False

        # Quit Logic
        if game_over and key_response == "quit":
            pygame.quit()
            sys.exit()

        draw_grid(surface)

        if not game_over:
            collision = snake.move()
            if collision:
                game_over = True

            head = snake.get_head_position()
            if head in snake.position[1:]:
                game_over = True

            if head == food.position:
                snake.length += 1
                score += 1
                food.random_pos()

        # Draw items on surface
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = font.render("Score {0}".format(score), True, black)
        screen.blit(text, (5, 10))

        # Game over logic
        if game_over:
            game_over_text = font.render(
                "Game Over! Press R to Restart or Q to Quit", True, black
            )
            screen.blit(game_over_text, (WIDTH // 2 - 225, HEIGHT // 2))

        pygame.display.update()


main()
