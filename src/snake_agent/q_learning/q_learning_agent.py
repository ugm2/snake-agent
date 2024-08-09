import logging
import os
import pickle
import random

from snake_game.constants import ACTION_SPACE

from ..utils import state_to_key
from .constants import (
    DISCOUNT_FACTOR,
    EXPLORATION_DECAY,
    EXPLORATION_RATE,
    LEARNING_RATE,
    LR_DECAY,
    MIN_EXPLORATION_RATE,
    MIN_LR,
)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))

class QLearningAgent:
    def __init__(self, action_space=ACTION_SPACE, state_space=None, train=True, learning_rate=LEARNING_RATE, discount_factor=DISCOUNT_FACTOR, 
                 exploration_rate=EXPLORATION_RATE, exploration_decay=EXPLORATION_DECAY, min_exploration_rate=MIN_EXPLORATION_RATE, 
                 lr_decay=LR_DECAY, min_lr=MIN_LR):
        self.action_space = action_space
        self.state_space = state_space
        self.learning_rate = learning_rate
        self.lr_decay = lr_decay
        self.min_lr = min_lr
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.q_table = {}
        self.train = train

    def get_action(self, state):
        state_key = state_to_key(state)
        if self.train and random.uniform(0, 1) < self.exploration_rate:
            action = random.choice(self.action_space)
        else:
            action = self.get_best_action(state_key)
        logging.debug(f'State: {state}, Action: {action}, Exploration rate: {self.exploration_rate}')
        return action

    def get_best_action(self, state_key):
        if state_key not in self.q_table:
            logging.debug(f'State not found in Q-table: {state_key}')
            return random.choice(self.action_space)
        logging.debug(f'ACTION FOUND FOR STATE: {state_key}')
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_value(self, state, action, reward, next_state):
        if not self.train:
            return
        
        state_key = state_to_key(state)
        next_state_key = state_to_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.action_space}

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0.0 for action in self.action_space}

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_state_key].values())

        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state_key][action] = new_value

        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
        self.learning_rate = max(self.min_lr, self.learning_rate * self.lr_decay)
        logging.debug(f'Updated Q-value for state: {state_key}, action: {action}, reward: {reward}, next state: {next_state_key}, new Q-value: {new_value}')
        
    def save_q_table(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)
        logging.info(f'Q-table saved to {filepath}')
        
    def load_q_table(self, filepath):
        with open(filepath, "rb") as f:
            self.q_table = pickle.load(f)
        logging.info(f'Q-table loaded from {filepath}')