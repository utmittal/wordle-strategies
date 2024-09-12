from abc import ABC, abstractmethod


class Player(ABC):

    @abstractmethod
    def get_next_guess(self, game_state):
        pass
