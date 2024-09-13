from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, wd):
        pass

    @abstractmethod
    def get_next_guess(self, game_state, turn):
        pass

    @staticmethod
    @abstractmethod
    def get_name():
        pass
