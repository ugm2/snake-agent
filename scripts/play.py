import argparse
import pickle

from snake_agent.q_learning.q_learning_agent import QLearningAgent
from snake_game.game import Game


def main(agent_file=None):
    agent = None
    if agent_file:
        # Load the trained agent
        with open(agent_file, "rb") as f:
            q_table = pickle.load(f)
        action_space = ["UP", "DOWN", "LEFT", "RIGHT"]
        agent = QLearningAgent(action_space=action_space, state_space=None, train=False)
        agent.q_table = q_table
        print("Agent loaded successfully.")

    # Initialize the game with or without an agent
    game = Game(agent=agent, render=True)
    game.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Snake game manually or with a trained agent.")
    parser.add_argument("--agent", type=str, help="Path to the trained agent file.")
    args = parser.parse_args()
    main(args.agent)