import os

from snake_agent.q_learning.constants import CHECKPOINT_INTERVAL, Q_TABLE_SAVE_PATH
from snake_game.game import Game
from tqdm import tqdm


class Trainer:
    def __init__(self, agent, episodes=1000, save_path=Q_TABLE_SAVE_PATH):
        self.agent = agent
        self.episodes = episodes
        self.save_path = save_path

    def train(self):
        progress_bar = tqdm(range(self.episodes), 
                            dynamic_ncols=True, 
                            bar_format="Episode {n_fmt}/{total_fmt} ({elapsed}<{remaining}) [{percentage:3.0f}%] {postfix}")
        for episode in progress_bar:
            game = Game(agent=self.agent, render=False)
            total_reward, score = game.run()
            progress_bar.set_postfix({
                'total_reward': total_reward,
                'score': score,
                'lr': f"{self.agent.learning_rate:.6f}",
                'discount_factor': f"{self.agent.discount_factor:.6f}",
                'exploration_rate': f"{self.agent.exploration_rate:.6f}",
                'exploration_decay': f"{self.agent.exploration_decay:.6f}",
                'exploration_min_rate': f"{self.agent.exploration_rate:.6f}"
            })
            
            # Save checkpoint
            if (episode + 1) % CHECKPOINT_INTERVAL == 0:
                checkpoint_path = os.path.join(self.save_path, f"checkpoint_{episode + 1}.pkl")
                self.agent.save_q_table(checkpoint_path)

        self.agent.save_q_table(os.path.join(self.save_path, "q_table.pkl"))