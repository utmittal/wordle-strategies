import random

from game_simulator import TOTAL_LETTERS


def _parse_words_from_file(path: str):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return [w.strip().upper() for w in lines]


class WordleDictionary:
    def __init__(self):
        self.__valid_guesses = _parse_words_from_file('database/valid_guesses.txt')
        self.__valid_guesses_set = set(self.__valid_guesses)
        self.__valid_puzzles = _parse_words_from_file('database/valid_puzzles.txt')

        # create index of words containing a specific letter
        self.__letter_index = {}
        for g in self.__valid_guesses:
            letters = list(g)
            for l in letters:
                if l in self.__letter_index:
                    self.__letter_index[l].add(g)
                else:
                    self.__letter_index[l] = {g}

        # create index of words containing a specific letter in a specific position
        self.__letter_pos_index = {}
        for w in self.__valid_guesses:
            letters = list(w)
            for l, i in zip(letters, range(TOTAL_LETTERS)):
                if l not in self.__letter_pos_index:
                    self.__letter_pos_index[l] = {i: {w}}
                else:
                    letter_dic = self.__letter_pos_index[l]
                    if i not in letter_dic:
                        letter_dic[i] = {w}
                    else:
                        letter_dic[i].add(w)

    def get_random_puzzle(self) -> str:
        return random.choice(self.__valid_puzzles)

    def get_all_puzzles(self) -> list[str]:
        return self.__valid_puzzles

    def contains(self, word: str) -> bool:
        if word.upper() in self.__valid_guesses:
            return True
        else:
            return False

    def get_random(self) -> str:
        return random.choice(self.__valid_guesses)

    def get_filtered_guesses(self, greens: list[tuple[str, int]] = None,
                             includes: list = None, excludes: set = None) -> set[str]:
        """
        :param greens: Known green letter positions
        :param includes: Known letters that occur in the word
        :param excludes: Known letters that do not occur in the word
        :return: set of words
        """
        if greens is None:
            greens = []
        if includes is None:
            includes = []
        if excludes is None:
            excludes = set()

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

        filtered_set = self.__valid_guesses_set.copy()
        # print("1" + str(filtered_set))
        if len(valid_guesses_greens) > 0:
            filtered_set.intersection_update(valid_guesses_greens)
            # print("2" + str(filtered_set))
        if len(guesses_includes) > 0:
            filtered_set.intersection_update(guesses_includes)
            # print("3" + str(filtered_set))
        if len(guesses_excludes) > 0:
            filtered_set.difference_update(guesses_excludes)

        return filtered_set

    def get_filtered_guesses_v2(self, greens: list[tuple[str, int]] = None,
                                yellows: dict[str:int] = None, greys: set = None) -> set[str]:
        """
        :param greens: Known green letter positions
        :param yellows: Known yellow letter positions
        :param greys: Known letters that do not occur in the word
        :return: set of words
        """
        if greens is None:
            greens = []
        if yellows is None:
            yellows = {}
        if greys is None:
            greys = set()

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

        filtered_set = self.__valid_guesses_set.copy()
        # print("1" + str(filtered_set))
        if len(valid_guesses_greens) > 0:
            filtered_set.intersection_update(valid_guesses_greens)
            # print("2" + str(filtered_set))
        if len(valid_guesses_yellow) > 0:
            filtered_set.intersection_update(valid_guesses_yellow)
            # print("3" + str(filtered_set))
        if len(valid_guesses_grey) > 0:
            filtered_set.difference_update(valid_guesses_grey)
            # print("4" + str(filtered_set))

        return filtered_set
