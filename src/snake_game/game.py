import logging
import os

import pygame

from .board import Board
from .constants import BOARD_HEIGHT, BOARD_WIDTH, DIRECTION_MAP, GRID_SIZE, SNAKE_SPEED
from .food import Food
from .player import DEFAULT_PLAYER_NAME, Player
from .reward import Reward
from .snake import Snake

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

class Game:
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT, grid_size=GRID_SIZE, agent=None, render=True):
        self.render = render
        if self.render:
            pygame.init()
            self.clock = pygame.time.Clock()
        self.board = Board(width, height, grid_size, self.render)
        self.snake = Snake(grid_size)
        self.food = Food(grid_size, self.board)
        self.player = Player(DEFAULT_PLAYER_NAME)
        self.snake_speed = SNAKE_SPEED
        self.running = True
        self.agent = agent
        self.reward_system = Reward()
        
    def get_state(self):
        snake_head = self.snake.positions[0]
        snake_body = self.snake.positions[1:]
        food_position = self.food.position

        # Relative food position
        food_dx = (food_position[0] - snake_head[0]) / self.board.width
        food_dy = (food_position[1] - snake_head[1]) / self.board.height

        # Direction encoding (one-hot)
        direction_one_hot = [0, 0, 0, 0]
        direction_index = {(0, -1): 0, (0, 1): 1, (-1, 0): 2, (1, 0): 3}[self.snake.direction]
        direction_one_hot[direction_index] = 1

        # Danger detection
        danger = [
            self.is_collision(snake_head[0], snake_head[1] - self.snake.grid_size),  # Up
            self.is_collision(snake_head[0], snake_head[1] + self.snake.grid_size),  # Down
            self.is_collision(snake_head[0] - self.snake.grid_size, snake_head[1]),  # Left
            self.is_collision(snake_head[0] + self.snake.grid_size, snake_head[1]),   # Right
            self.is_collision(snake_head[0] - self.snake.grid_size, snake_head[1] - self.snake.grid_size),  # Up-Left
            self.is_collision(snake_head[0] + self.snake.grid_size, snake_head[1] - self.snake.grid_size),  # Up-Right
            self.is_collision(snake_head[0] - self.snake.grid_size, snake_head[1] + self.snake.grid_size),  # Down-Left
            self.is_collision(snake_head[0] + self.snake.grid_size, snake_head[1] + self.snake.grid_size)   # Down-Right
        ]

        # Body representation (nearest 3 segments)
        body_relative = []
        for segment in snake_body[:3]:
            rel_x = (segment[0] - snake_head[0]) / self.board.width
            rel_y = (segment[1] - snake_head[1]) / self.board.height
            body_relative.append((rel_x, rel_y))

        # Pad body_relative if less than 3 segments
        body_relative += [(0, 0)] * (3 - len(body_relative))

        state = (
            food_dx,
            food_dy,
            *direction_one_hot,
            *danger,
            *[coord for segment in body_relative for coord in segment]
        )

        logging.debug(f'Game state: {state}')
        return state

    def is_collision(self, x, y):
        return (x < 0 or x >= self.board.width or
                y < 0 or y >= self.board.height or
                (x, y) in self.snake.positions[1:])
    
    def update(self):
        if self.agent:
            current_state = self.get_state()
            action = self.agent.get_action(current_state)

            action_to_direction = {
                "UP": (0, -1),
                "DOWN": (0, 1),
                "LEFT": (-1, 0),
                "RIGHT": (1, 0),
            }
            self.snake.set_direction(action_to_direction[action])

        self.snake.move()

        snake_has_collided_with_food = self.snake.has_collided_with_food(self.food.position, self.food.size)
        if snake_has_collided_with_food:
            self.snake.grow()
            self.food.spawn_new_food()
            self.player.increment_score()

        snake_has_collided = self.snake.has_collided_with_wall(self.board.width, self.board.height) or self.snake.has_collided_with_self()
        if snake_has_collided:
            self.running = False
            
        reward = self.reward_system.compute_reward(self, snake_has_collided_with_food, snake_has_collided)
        
        if self.agent:    
            logging.debug(f'Action: {action}, Reward: {reward}')
            next_state = self.get_state()    
            self.agent.update_q_value(current_state, action, reward, next_state)

        return reward

    def handle_input(self):
        if self.render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif not self.agent and event.type == pygame.KEYDOWN:
                    if event.key in DIRECTION_MAP:
                        self.snake.set_direction(DIRECTION_MAP[event.key])

    def draw(self):
        if self.render:
            self.board.draw_background()
            self.board.draw_food(self.food.position, self.food.size)
            self.board.draw_snake(self.snake.positions)
            pygame.display.flip()

    def run(self):
        total_reward = 0
        while self.running:
            self.handle_input()
            reward = self.update()
            total_reward += reward
            self.draw()
            if self.render:
                self.clock.tick(self.snake_speed)
                pygame.event.pump()

        if self.render:
            pygame.quit()
        
        logging.debug(f'Total reward: {total_reward}, Score: {self.player.get_score()}')
        return total_reward, self.player.get_score()