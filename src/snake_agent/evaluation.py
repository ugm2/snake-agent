import csv
import logging
import os
from statistics import mean

from snake_game.game import Game

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))

class Evaluator:
    def __init__(self, agent, episodes=100, save_path="models/q_learning/"):
        self.agent = agent
        self.episodes = episodes
        self.runs_save_path = os.path.join(save_path, "evaluation_runs.csv")
        self.metrics_save_path = os.path.join(save_path, "evaluation_metrics.csv")

    def evaluate(self):
        results = []
        for episode in range(self.episodes):
            game = Game(agent=self.agent, render=False)
            total_reward, score = game.run()
            results.append((total_reward, score))
            print(f'Episode {episode + 1}/{self.episodes} evaluated with total reward: {total_reward}, score: {score}')
        
        self.save_runs(results)
        return self.save_metrics(results)

    def save_runs(self, results):
        with open(self.runs_save_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "Total Reward", "Score"])
            for i, (total_reward, score) in enumerate(results):
                writer.writerow([i + 1, total_reward, score])
        logging.info(f'Evaluation runs saved to {self.runs_save_path}')

    def save_metrics(self, results):
        total_rewards, scores = zip(*results)
        metrics = {
            "Average Total Reward": mean(total_rewards),
            "Average Score": mean(scores),
            "Maximum Total Reward": max(total_rewards),
            "Maximum Score": max(scores),
            "Minimum Total Reward": min(total_rewards),
            "Minimum Score": min(scores)
        }
        
        with open(self.metrics_save_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            for key, value in metrics.items():
                writer.writerow([key, value])
        logging.info(f'Evaluation metrics saved to {self.metrics_save_path}')
        return metrics