from dataclasses import dataclass
from typing import ClassVar

DEFAULT_PLAYER_NAME = "Player 1"
SCORE_INCREMENT = 1

@dataclass
class Player:
    name: str = DEFAULT_PLAYER_NAME
    score: int = 0

    DEFAULT_NAME: ClassVar[str] = DEFAULT_PLAYER_NAME

    def increment_score(self) -> None:
        """Increment the player's score by the defined increment value."""
        self.score += SCORE_INCREMENT

    def get_score(self) -> int:
        """Return the player's current score."""
        return self.score