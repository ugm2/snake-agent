# scripts/train_agent.py

import argparse

from snake_agent.evaluation import Evaluator
from snake_agent.q_learning.constants import (
    Q_ALGORITHM_EVALUATION_PATH,
    Q_TABLE_SAVE_PATH,
    TRAINING_EPISODES,
)
from snake_agent.q_learning.q_learning_agent import QLearningAgent
from snake_agent.trainer import Trainer
from snake_game.constants import ACTION_SPACE


def main():
    parser = argparse.ArgumentParser(description='Train a Q-learning agent')
    parser.add_argument('--model', type=str, help='Path to the Q-table model to load')
    args = parser.parse_args()

    agent = QLearningAgent(action_space=ACTION_SPACE, state_space=None)
    if args.model:
        agent.load_q_table(args.model)
    
    trainer = Trainer(agent=agent, episodes=TRAINING_EPISODES, save_path=Q_TABLE_SAVE_PATH)
    trainer.train()
    
    # Evaluate the agent after training
    evaluator = Evaluator(agent=agent, episodes=1000, save_path=Q_ALGORITHM_EVALUATION_PATH)
    metrics = evaluator.evaluate()
    print(metrics)

if __name__ == "__main__":
    main()