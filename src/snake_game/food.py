import random

from .constants import FOOD_REWARD, FOOD_SIZE_RATIO


class Food:
    def __init__(self, grid_size, board, reward=FOOD_REWARD):
        self.grid_size = grid_size
        self.board = board
        self.size = int(grid_size * FOOD_SIZE_RATIO)
        self.position = self._get_random_food_position()
        self.reward = reward
        

    def _get_random_food_position(self):
        return (
            random.randint(0, (self.board.width // self.grid_size) - 1) * self.grid_size + (self.grid_size - self.size) // 2,
            random.randint(0, (self.board.height // self.grid_size) - 1) * self.grid_size + (self.grid_size - self.size) // 2
        )

    def spawn_new_food(self):
        self.position = self._get_random_food_position()
        