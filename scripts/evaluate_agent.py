import argparse
import pickle

from snake_agent.evaluation import Evaluator
from snake_agent.q_learning.constants import Q_ALGORITHM_EVALUATION_PATH
from snake_agent.q_learning.q_learning_agent import QLearningAgent
from snake_game.constants import ACTION_SPACE


def main(agent_file, episodes, save_path):
    with open(agent_file, "rb") as f:
        q_table = pickle.load(f)
    
    agent = QLearningAgent(action_space=ACTION_SPACE, train=False)
    agent.q_table = q_table
    
    evaluator = Evaluator(agent=agent, episodes=episodes, save_path=save_path)
    metrics = evaluator.evaluate()
    print(metrics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a trained Q-learning agent")
    parser.add_argument("--agent", type=str, required=True, help="Path to the trained agent file")
    parser.add_argument("--episodes", type=int, default=10000, help="Number of evaluation episodes")
    parser.add_argument("--save_path", type=str, default=Q_ALGORITHM_EVALUATION_PATH, help="Path to save the evaluation results")
    args = parser.parse_args()
    
    main(args.agent, args.episodes, args.save_path)