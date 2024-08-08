
from .constants import COLLISION_PENALTY, STEP_PENALTY


class Reward:
    def __init__(self, collision_penalty=COLLISION_PENALTY, step_penalty=STEP_PENALTY):
        self.collision_penalty = collision_penalty
        self.step_penalty = step_penalty

    def compute_reward(self, game, snake_has_collided_with_food, snake_has_collided):
        reward = self.step_penalty
        if snake_has_collided_with_food:
            reward = game.food.reward
        elif snake_has_collided:
            reward = self.collision_penalty
        return reward