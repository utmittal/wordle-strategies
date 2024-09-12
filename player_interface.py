from abc import ABC, abstractmethod, abstractstaticmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, wd):
        pass

    @abstractmethod
    def get_next_guess(self, game_state, turn):
        pass

    @abstractstaticmethod
    def get_name():
        pass
