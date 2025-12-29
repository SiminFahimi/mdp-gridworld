import pygame
import random

PINK = (255, 127, 127)
BLACK = (0, 0, 0)
DARKORCHID = (153, 50, 204)
THISTLE = (216, 191, 216)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Grid:
    def __init__(self, screen, screen_height, screen_width, cell_size, wall_density):
        self.walls = []
        self.wall_density = wall_density
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.cell_size = cell_size
        self.screen = screen
        self.add_walls_hell_heaven()

    def add_walls_hell_heaven(self):
        valid_cells = [
            (i, j)
            for i in range(0, self.screen_width, self.cell_size)
            for j in range(0, self.screen_height, self.cell_size)
        ]
        count = 2 + round(
            (self.screen_height / self.cell_size * self.screen_width / self.cell_size)
            * self.wall_density
        )
        lst = random.sample(valid_cells, count)
        self.hell = lst.pop(0)
        self.heaven = lst.pop(0)
        self.walls = lst

    def draw(self):
        if self.screen is None:
            return
        self.screen.fill(DARKORCHID)

        # walls
        for wall in self.walls:
            pygame.draw.rect(
                self.screen,
                BLACK,
                (wall[0], wall[1], self.cell_size, self.cell_size),
            )

        # grid lines
        for i in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(
                self.screen, PINK, (i, 0), (i, self.screen_height), 1
            )
        for j in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(
                self.screen, PINK, (0, j), (self.screen_width, j), 1
            )

        # hell and heaven
        pygame.draw.rect(
            self.screen,
            RED,
            (self.hell[0], self.hell[1], self.cell_size, self.cell_size),
        )
        pygame.draw.rect(
            self.screen,
            GREEN,
            (self.heaven[0], self.heaven[1], self.cell_size, self.cell_size),
        )
