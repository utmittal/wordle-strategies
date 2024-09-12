from player_interface import Player
from wordle_dictionary import WordleDictionary
from game_simulator import State
import random


class PlayerRandomGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word which
    satisfies the known information. I.e. if the first guess revealed 1 yellow letter, it will make a random guess from
    a list of words which have the yellow letter.
    """

    def __init__(self, debug=False):
        self.__wd = WordleDictionary()
        self.__debug = debug
        self.__name = "RandomGuesser"

    def get_next_guess(self, game_state):
        green_dic, includes, excludes = self.__get_known_info(game_state)
        possible_guesses = self.__wd.get_filtered_guesses(greens=green_dic, includes=includes, excludes=excludes)

        if self.__debug:
            print("Greens - " + str(green_dic) + " | Includes - " + str(includes) + " | Excludes - " + str(excludes))
            print("Possible choices - " + str(len(possible_guesses)))

        return random.choice(possible_guesses)

    def __get_known_info(self, game_state):
        # Let's abuse python's loose typing
        green_dic = {}
        includes = []
        excludes = set()

        # Because of the way this player plays, the last played row will always have the most
        # up-to-date information about yellows and greens. But we need greys from all rows.
        latest_row_index = None
        for row, i in zip(game_state, range(0, 6)):
            all_blank = True
            for elem in row:
                letter = elem[0]
                color = elem[1]
                if color == State.grey:
                    excludes.add(letter)

                if color != State.blank:
                    all_blank = False

            if all_blank:
                latest_row_index = i - 1
                # means there is no more info in the rest of the rows anyway
                break

        for elem, i in zip(game_state[latest_row_index], range(0, 5)):
            letter = elem[0]
            color = elem[1]

            if color == State.green:
                # Should never happen
                if i in green_dic and green_dic[i] != letter:
                    raise Exception("Something has gone very wrong.")
                else:
                    green_dic[i] = letter
            elif color == State.yellow:
                includes.append(letter)

        return green_dic, includes, excludes

    def get_name(self):
        return self.__name
