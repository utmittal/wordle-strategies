import random
from itertools import combinations
from pathlib import Path

from util.indexers import get_letter_index, get_letter_position_index, get_repeated_letter_position_index
from util.project_path import project_path
from util.set_operations import intersect_all


class WordleDictionary:
    __valid_guesses: list[str]
    __valid_guesses_set: set[str]
    __valid_puzzles: list[str]

    __letter_index: dict[str, set[str]]
    __letter_pos_index: dict[str, dict[int, set[str]]]
    __repeated_letter_index: dict[str, dict[tuple[int, ...], set[str]]]

    def __init__(self):
        self.__valid_guesses = WordleDictionary.__parse_words_from_file('database/valid_guesses.txt')
        self.__valid_guesses_set = set(self.__valid_guesses)
        self.__valid_puzzles = WordleDictionary.__parse_words_from_file('database/valid_puzzles.txt')

        self.__letter_index = get_letter_index(self.__valid_guesses)
        self.__letter_pos_index = get_letter_position_index(self.__valid_guesses)
        self.__repeated_letter_index = get_repeated_letter_position_index(self.__valid_guesses)

    def get_random_puzzle(self) -> str:
        return random.choice(self.__valid_puzzles)

    def get_all_puzzles(self) -> list[str]:
        return self.__valid_puzzles

    def get_all_words(self) -> list[str]:
        return self.__valid_guesses

    def contains(self, word: str) -> bool:
        if word.upper() in self.__valid_guesses:
            return True
        else:
            return False

    def get_random_word(self) -> str:
        return random.choice(self.__valid_guesses)

    def get_filtered_guesses(self, greens: list[tuple[str, int]],
                             includes: list, excludes: set) -> set[str]:
        """
        :param greens: Known green letter positions
        :param includes: Known letters that occur in the word
        :param excludes: Known letters that do not occur in the word
        :return: set of words
        """
        # short circuit
        if greens == [] and includes == [] and excludes == set():
            return set(self.__valid_guesses)

        # all valid guesses based on the position of greens
        green_sets = []
        for tup in greens:
            letter, position = tup
            green_sets.append(self.__letter_pos_index[letter][position])
        if len(green_sets) > 0:
            valid_guesses_greens = set.intersection(*green_sets)
        else:
            valid_guesses_greens = set()

        # all valid guesses that have an excludes letter in them
        excludes_sets = [self.__letter_index[e.upper()] for e in excludes]
        if len(excludes_sets) > 0:
            guesses_excludes = set.union(*excludes_sets)
        else:
            guesses_excludes = set()

        # all valid guesses that have an includes letter in them
        includes_sets = [self.__letter_index[i.upper()] for i in includes]
        if len(includes_sets) > 0:
            guesses_includes = set.union(*includes_sets)
        else:
            guesses_includes = set()

        filtered_set = intersect_all(self.__valid_guesses_set, valid_guesses_greens, guesses_includes)
        if len(guesses_excludes) > 0:
            filtered_set.difference_update(guesses_excludes)

        return filtered_set

    def get_filtered_guesses_v2(self, greens: list[tuple[str, int]],
                                yellows: dict[str, list[int]], greys: set) -> set[str]:
        """
        :param greens: Known green letter positions
        :param yellows: Known yellow letter positions
        :param greys: Known letters that do not occur in the word
        :return: set of words
        """
        # short circuit
        if greens == [] and yellows == {} and greys == set():
            return set(self.__valid_guesses)

        # all valid guesses based on the position of greens
        green_sets = []
        for tup in greens:
            letter, position = tup
            green_sets.append(self.__letter_pos_index[letter][position])
        if len(green_sets) > 0:
            valid_guesses_greens = set.intersection(*green_sets)  # could be empty
        else:
            valid_guesses_greens = set()

        # all valid guesses based on position of yellows
        yellow_sets = []  # all sets for yellow letters, where each set corresponds to a single letter
        for letter in yellows:
            single_letter_sets = []  # all sets for a single letter, where each set represents a different position
            for position in yellows[letter]:
                single_letter_sets.append(self.__letter_pos_index[letter.upper()][position])
            yellow_sets.append(set.union(*single_letter_sets))
        if len(yellow_sets) > 0:
            valid_guesses_yellow = set.intersection(*yellow_sets)  # could be empty
        else:
            valid_guesses_yellow = set()

        # all valid guesses that have a grey letter in them
        grey_sets = [self.__letter_index[e.upper()] for e in greys]
        if len(grey_sets) > 0:
            valid_guesses_grey = set.union(*grey_sets)  # could be empty
        else:
            valid_guesses_grey = set()

        filtered_set = intersect_all(self.__valid_guesses_set, valid_guesses_greens, valid_guesses_yellow)
        if len(valid_guesses_grey) > 0:
            filtered_set.difference_update(valid_guesses_grey)
            # print("4" + str(filtered_set))

        return filtered_set

    def get_filtered_guesses_v3(self, greens: list[tuple[str, int]],
                                single_yellows: dict[str, list[int]],
                                double_yellows: dict[str, list[int]],
                                greys: set) -> set[str]:
        """
        :param greens: Known green letter positions
        :param single_yellows: Known yellow letter positions for yellows that occur only once
        :param double_yellows: Known yellow letter positions for yellows that occur twice
        :param greys: Known letters that do not occur in the word
        :return: set of words
        """
        # short circuit
        if greens == [] and single_yellows == {} and double_yellows == {} and greys == set():
            return set(self.__valid_guesses)

        # all valid guesses based on the position of greens
        green_sets = []
        for tup in greens:
            letter, position = tup
            green_sets.append(self.__letter_pos_index[letter][position])
        if len(green_sets) > 0:
            valid_guesses_greens = set.intersection(*green_sets)  # could be empty
        else:
            valid_guesses_greens = set()

        # all valid guesses based on position of yellows
        yellow_sets = []  # all sets for yellow letters, where each set corresponds to a single letter
        for letter in single_yellows:
            single_letter_sets = []  # all sets for a single letter, where each set represents a different position
            for position in single_yellows[letter]:
                single_letter_sets.append(self.__letter_pos_index[letter.upper()][position])
            yellow_sets.append(set.union(*single_letter_sets))
        if len(yellow_sets) > 0:
            valid_guesses_yellow = set.intersection(*yellow_sets)  # could be empty
        else:
            valid_guesses_yellow = set()

        # all valid guesses based on position of double yellows
        double_yellow_sets = []
        for letter in double_yellows:
            combos = combinations(sorted(double_yellows[letter]), 2)
            specific_letter_sets = []
            for pos in combos:
                if pos in self.__repeated_letter_index[letter.upper()]:
                    specific_letter_sets.append(self.__repeated_letter_index[letter.upper()][pos])
            double_yellow_sets.append(set.union(*specific_letter_sets))
        if len(double_yellow_sets) > 0:
            valid_guesses_double_yellow = set.intersection(*double_yellow_sets)
        else:
            valid_guesses_double_yellow = set()

        # all valid guesses that have a grey letter in them
        grey_sets = [self.__letter_index[e.upper()] for e in greys]
        if len(grey_sets) > 0:
            valid_guesses_grey = set.union(*grey_sets)  # could be empty
        else:
            valid_guesses_grey = set()

        filtered_set = intersect_all(self.__valid_guesses_set, valid_guesses_greens, valid_guesses_yellow,
                                     valid_guesses_double_yellow)
        if len(valid_guesses_grey) > 0:
            filtered_set.difference_update(valid_guesses_grey)
            # print("4" + str(filtered_set))

        return filtered_set

    @staticmethod
    def __parse_words_from_file(path: Path | str) -> list[str]:
        path = project_path(path)
        with open(path, 'r') as f:
            lines = f.read().splitlines()
        return [w.strip().upper() for w in lines]
