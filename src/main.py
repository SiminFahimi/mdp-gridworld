import sys

import pygame

from algorithms  import policy_iteration
# from algorithms import value_iteration

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CELL_SIZE,
    WALL_DENSITY,
    NOISE,
    DISCOUNT_FACTOR,
)
from grid import Grid, THISTLE
from mdp import MDP


def run():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MDP GridWorld - policy Iteration")
    # or pygame.display.set_caption("MDP GridWorld - value Iteration")

    grid = Grid(
        screen,
        SCREEN_HEIGHT,
        SCREEN_WIDTH,
        CELL_SIZE,
        WALL_DENSITY,
    )
    mdp = MDP(grid, NOISE, DISCOUNT_FACTOR)
    values = policy_iteration(mdp)
    # or value=value_iteration(mdp)

    font = pygame.font.SysFont("Arial", 12)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        grid.draw()

        for position, val, action in values:
            text_surface = font.render(f"{val} {action}", True, THISTLE)
            x = position[0] + (grid.cell_size // 2)
            y = position[1] + (grid.cell_size // 2)
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run()
