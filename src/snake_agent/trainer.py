
from snake_game.game import Game


class Trainer:
    def __init__(self, agent, episodes=1000, save_path="q_table.pkl"):
        self.agent = agent
        self.episodes = episodes
        self.save_path = save_path

    def train(self):
        for episode in range(self.episodes):
            game = Game(agent=self.agent, render=False)
            total_reward, score = game.run()
            print(f'Episode {episode + 1}/{self.episodes} completed with total reward: {total_reward},'
                  f'score: {score}, lr: {self.agent.learning_rate}, '
                  f'discount factor: {self.agent.discount_factor}, '
                  f'exploration rate: {self.agent.exploration_rate}, '
                  f'exploration decay: {self.agent.exploration_decay}, '
                  f'exploration min rate: {self.agent.exploration_rate}')

        self.agent.save_q_table(self.save_path)