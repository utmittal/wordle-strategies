from mimetypes import knownfiles

from player_interface import Player
from wordle_dictionary import WordleDictionary
from game_simulator import State


class PlayerRandomGuesser(Player):
    """
    This player will make a random guess on the first time. On subsequent turns, it will choose a random word which
    satisfies the known information. I.e. if the first guess revealed 1 yellow letter, it will make a random guess from
    a list of words which have the yellow letter.
    """

    def __init__(self):
        self.__wd = WordleDictionary()

    def get_next_guess(self, game_state):
        known_info = self.__get_known_info(game_state)

    def __get_known_info(self, game_state):
        # Let's abuse python's loose typing
        known_info = {0: None,
                      1: None,
                      2: None,
                      3: None,
                      4: None,
                      'includes': set(),
                      'excludes': set()}

        for row in game_state:
            for word, i in zip(row, range(0, 5)):
                letter = word[0]
                color = word[1]

                if color == State.green:
                    if known_info[i] is not None or known_info[i] != letter:
                        raise Exception("Something has gone very wrong.")
                    else:
                        known_info[i] = letter

                if color == State.yellow:
                    known_info['includes'].add(letter)

                if color == State.grey:
                    known_info['excludes'].add(letter)

        return known_info
