import random

from player_interface import Player
from wordle_dictionary import WordleDictionary
from game_simulator import State, TOTAL_LETTERS


class PlayerRandomGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word which
    satisfies the known information. I.e. if the first guess revealed 1 yellow letter, it will make a random guess from
    a list of words which have the yellow letter.

    Note: This player doesn't take into consideration the locations of the yellow letters. I.e. it doesn't try to avoid
    yellow locations that it has already tried.
    """
    __name = "RandomGuesser"

    def __init__(self, debug=False):
        self.__wd = WordleDictionary()
        self.__debug = debug
        self.__greens = {}
        self.__includes = []  # list because of double letters
        self.__excludes = set()

    @staticmethod
    def get_name():
        return PlayerRandomGuesser.__name

    def get_next_guess(self, game_state, turn):
        if turn == 0:
            return self.__wd.get_random()

        self.__update_known_info(game_state[turn - 1])
        possible_guesses = self.__wd.get_filtered_guesses(greens=self.__greens, includes=self.__includes,
                                                          excludes=self.__excludes)

        if self.__debug:
            print("Greens - " + str(self.__greens) + " | Includes - " + str(self.__includes) + " | Excludes - " + str(
                self.__excludes))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(possible_guesses)

    def __update_known_info(self, latest_row):
        new_includes = []
        new_greens = {}
        for elem, i in zip(latest_row, range(TOTAL_LETTERS)):
            letter = elem[0]
            color = elem[1]

            if color == State.grey:
                self.__excludes.add(letter)
                continue
            elif color == State.green:
                new_greens[i] = letter
            elif color == State.yellow:
                new_includes.append(letter)
            else:
                raise Exception("Something has gone very wrong.")

        self.__greens = new_greens
        self.__includes = new_includes
