import random

from players.player_interface import Player
from game_simulator import LetterState, TOTAL_LETTERS, GameState, GameLetter
from wordle_dictionary import WordleDictionary


class PlayerRandomGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word which
    satisfies the known information. I.e. if the first guess revealed 1 yellow letter, it will make a random guess from
    a list of words which have the yellow letter.

    Note: This player doesn't take into consideration the locations of the yellow letters. I.e. it doesn't try to avoid
    yellow locations that it has already tried.
    """
    __name = "RandomGuesser"

    def __init__(self, wd: WordleDictionary, debug: bool = False):
        self.__wd = wd
        self.__debug = debug
        self.__greens = []
        self.__yellows = []  # list because of double letters
        self.__greys = set()

    @staticmethod
    def get_name() -> str:
        return PlayerRandomGuesser.__name

    def get_next_guess(self, game_state: GameState, turn: int) -> str:
        if turn == 0:
            return self.__wd.get_random()

        self.__update_known_info(game_state.get_last_turn())
        possible_guesses = self.__wd.get_filtered_guesses(greens=self.__greens, includes=self.__yellows,
                                                          excludes=self.__greys)

        if self.__debug:
            print("Greens - " + str(self.__greens) + " | Includes - " + str(self.__yellows) + " | Excludes - " + str(
                self.__greys))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(list(possible_guesses))

    def __update_known_info(self, latest_row: list[GameLetter]) -> None:
        new_includes = []
        new_greens = []
        new_excludes = set()
        for game_letter, i in zip(latest_row, range(TOTAL_LETTERS)):
            if game_letter.color == LetterState.grey:
                new_excludes.add(game_letter.letter)
            elif game_letter.color == LetterState.green:
                new_greens.append((game_letter.letter, i))
            elif game_letter.color == LetterState.yellow:
                new_includes.append(game_letter.letter)
            else:
                raise Exception("Something has gone very wrong.")

        # We need this to handle the corner case where a double letter in a guess results in a yellow and grey.
        # If the letter is in yellow, we don't want to put it in grey.
        for ne in new_excludes:
            if ne not in new_includes and ne not in [t[0] for t in new_greens]:
                self.__greys.add(ne)

        self.__greens = new_greens
        self.__yellows = new_includes
