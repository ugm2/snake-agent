import pygame

from .constants import (
    BACKGROUND_COLOR,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    FOOD_COLOR,
    GRID_SIZE,
    SNAKE_COLOR,
)


class Board:
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT, grid_size=GRID_SIZE, render=True):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.render = render
        if self.render:
            self.window = pygame.display.set_mode((width, height))
        self.bg_color = BACKGROUND_COLOR

    def draw_background(self):
        if self.render:
            self.window.fill(self.bg_color)

    def draw_snake(self, positions):
        if self.render:
            for pos in positions:
                pygame.draw.rect(self.window, SNAKE_COLOR, pygame.Rect(pos[0], pos[1], self.grid_size, self.grid_size))

    def draw_food(self, food_position, size):
        if self.render:
            pygame.draw.rect(self.window, FOOD_COLOR, pygame.Rect(food_position[0], food_position[1], size, size))