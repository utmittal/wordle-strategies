import random

from player_interface import Player
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

    def __init__(self, wd, debug=False):
        self.__wd = wd
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
        new_excludes = set()
        for elem, i in zip(latest_row, range(TOTAL_LETTERS)):
            letter = elem[0]
            color = elem[1]

            if color == State.grey:
                new_excludes.add(letter)
            elif color == State.green:
                new_greens[letter] = i
            elif color == State.yellow:
                new_includes.append(letter)
            else:
                raise Exception("Something has gone very wrong.")

        # We need this to handle the corner case where a double letter in a guess results in a yellow and grey.
        # If the letter is in yellow, we don't want to put it in grey.
        for ne in new_excludes:
            if ne not in new_includes and ne not in new_greens:
                self.__excludes.add(ne)

        self.__greens = new_greens
        self.__includes = new_includes
