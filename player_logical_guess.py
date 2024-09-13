import random

from player_interface import Player
from game_simulator import State, TOTAL_LETTERS


class PlayerLogicalGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word that
    satisfies all the information it has learned so far. I.e. it will consider the position of yellows when making its
    guesses.
    """
    __name = "LogicalGuesser"

    def __init__(self, wd, debug=False):
        self.__wd = wd
        self.__debug = debug
        self.__greens = {}
        self.__greys = set()
        self.__yellows = {}

    @staticmethod
    def get_name():
        return PlayerLogicalGuesser.__name

    def get_next_guess(self, game_state, turn):
        if turn == 0:
            return self.__wd.get_random()

        self.__update_known_info(game_state, turn)
        possible_guesses = self.__wd.get_filtered_guesses_v2(greens=self.__greens, yellows=self.__yellows,
                                                             greys=self.__greys)

        if self.__debug:
            print("Greens - " + str(self.__greens) + " | Yellows - " + str(self.__yellows) + " | Excludes - " + str(
                self.__greys))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(possible_guesses)

    def __update_known_info(self, game_state, turn):
        current_yellows = []
        current_greens = {}
        new_greys = set()

        # evaluate current row
        for element, i in zip(game_state[turn - 1], range(TOTAL_LETTERS)):
            letter, color = element

            if color == State.grey:
                new_greys.add(letter)
            elif color == State.green:
                current_greens[letter] = i
            elif color == State.yellow:
                current_yellows.append(letter)
            else:
                raise Exception("Something has gone very wrong.")

        # We need this to handle the corner case where a double letter in a guess results in a yellow and grey.
        # If the letter is in yellow, we don't want to put it in grey.
        for ne in new_greys:
            if ne not in current_yellows and ne not in current_greens:
                self.__greys.add(ne)

        self.__greens = current_greens

        # Note: the logic below doesn't handle repeated yellows. Handling repeated letters properly might further
        # reduce the logical set of options available to us.
        self.__yellows = {}
        for inc in current_yellows:
            self.__yellows[inc] = [0, 1, 2, 3, 4]
        for row in game_state[:turn]:
            for el, i in zip(row, range(TOTAL_LETTERS)):
                letter, color = el
                if letter in current_yellows and (color == State.yellow or color == State.green):
                    self.__yellows[letter].remove(i)
