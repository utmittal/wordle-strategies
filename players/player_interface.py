from abc import ABC, abstractmethod

from game_simulator import GameState
from wordle_dictionary import WordleDictionary


class Player(ABC):
    @abstractmethod
    def __init__(self, wd: WordleDictionary, debug: bool):
        pass

    @abstractmethod
    def get_next_guess(self, game_state: GameState, turn: int) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass
