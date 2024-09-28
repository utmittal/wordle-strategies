from game_simulator import GameState
from players.player_interface import Player
from wordle_dictionary import WordleDictionary


class PlayerTrueRandom(Player):
    """
    Returns a random guess every time. Does not consider game state at any point.
    """
    __name = 'TrueRandom'

    __wd: WordleDictionary
    __debug: bool

    def __init__(self, wd: WordleDictionary, debug: bool):
        self.__wd = wd
        self.__debug = debug

    def get_next_guess(self, game_state: GameState, turn: int) -> str:
        return self.__wd.get_random_word()

    @staticmethod
    def get_name() -> str:
        return PlayerTrueRandom.__name
