from typing import Dict, Tuple

import pygame

# Board constants
BOARD_WIDTH = 400
BOARD_HEIGHT = 400
GRID_SIZE = 20
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Snake constants
INITIAL_SNAKE_POSITION = (100, 50)
SNAKE_COLOR = (0, 255, 0)  # Green

# Food constants
FOOD_COLOR = (213, 50, 80)  # Red
FOOD_SIZE_RATIO = 0.5  # Food size is half of the grid size

# Game constants
SNAKE_SPEED = 5
COLLISION_PENALTY = -100
STEP_PENALTY = -1
FOOD_REWARD = 200
MIN_REWARD = -2000

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_MAP: Dict[int, Tuple[int, int]] = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

ACTION_SPACE = ["UP", "DOWN", "LEFT", "RIGHT"]