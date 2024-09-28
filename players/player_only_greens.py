import random

from game_simulator import GameState, GameLetter, LetterState
from players.player_interface import Player
from wordle_dictionary import WordleDictionary


class PlayerOnlyGreens(Player):
    """
    Only considers green letters when choosing the next guess. Maintains the current greens, i.e. if it gets a green,
    it will use it in the next word.
    """
    __name = "OnlyGreens"

    __wd: WordleDictionary
    __debug: bool

    def __init__(self, wd: WordleDictionary, debug: bool):
        self.__wd = wd
        self.__debug = debug

    def get_next_guess(self, game_state: GameState, turn: int) -> str:
        if turn == 0:
            return self.__wd.get_random_word()

        green_positions = PlayerOnlyGreens.__get_green_positions(game_state.get_last_turn())
        possible_guesses = self.__wd.get_filtered_guesses_v3(green_positions, {}, {}, set())

        return random.choice(list(possible_guesses))

    @staticmethod
    def __get_green_positions(latest_row: list[GameLetter]) -> list[tuple[str, int]]:
        green_positions = []
        for i, letter in enumerate(latest_row):
            if letter.color == LetterState.green:
                green_positions.append((letter.letter, i))

        return green_positions

    @staticmethod
    def get_name() -> str:
        return PlayerOnlyGreens.__name
