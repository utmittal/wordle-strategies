import random
from game_simulator import TOTAL_LETTERS


def _parse_words_from_file(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return [w.strip().upper() for w in lines]


class WordleDictionary:
    def __init__(self):
        self.__valid_guesses = _parse_words_from_file('database/valid_guesses.txt')
        self.__valid_puzzles = _parse_words_from_file('database/valid_puzzles.txt')

        # create index of words containing a specific letter in a specific position
        self.__nested_index = {}
        for w in self.__valid_guesses:
            letters = list(w)
            for l, i in zip(letters, range(TOTAL_LETTERS)):
                if l not in self.__nested_index:
                    self.__nested_index[l] = {i: {w}}
                else:
                    letter_dic = self.__nested_index[l]
                    if i not in letter_dic:
                        letter_dic[i] = {w}
                    else:
                        letter_dic[i].add(w)

    def get_random_puzzle(self):
        return random.choice(self.__valid_puzzles)

    def get_all_puzzles(self):
        return self.__valid_puzzles

    def contains(self, word):
        if word.upper() in self.__valid_guesses:
            return True
        else:
            return False

    def get_random(self):
        return random.choice(self.__valid_guesses)

    def get_filtered_guesses(self, greens=None,
                             includes=None, excludes=None):
        if greens is None:
            greens = {}
        if includes is None:
            includes = []
        if excludes is None:
            excludes = set()

        # short circuit
        if greens == {} and includes == [] and excludes == set():
            return self.__valid_guesses

        # all valid guesses based on the position of greens
        green_sets = [self.__nested_index[g.upper()][greens[g]] for g in greens]
        valid_guesses_greens = None
        if len(green_sets) == 0:
            valid_guesses_greens = set(self.__valid_guesses)
        else:
            valid_guesses_greens = set.union(*green_sets)

        # list of dictionaries for excludes letters
        excludes_position_indexed_dictionaries = [self.__nested_index[e.upper()] for e in excludes]
        guesses_excludes = None
        if len(excludes_position_indexed_dictionaries) == 0:
            guesses_excludes = set()
        else:
            excludes_individual_sets = []
            for ed in excludes_position_indexed_dictionaries:
                excludes_individual_sets.append(set.union(*[ed[pos] for pos in ed]))
            guesses_excludes = set.union(*[e for e in excludes_individual_sets])

        valid_guesses_greens_excludes = valid_guesses_greens.difference(guesses_excludes)

        filtered_guesses = []
        for word in valid_guesses_greens_excludes:
            letters = list(word.upper())

            if self.__eval_word(letters, includes):
                filtered_guesses.append(word)

        return filtered_guesses

    @staticmethod
    def __eval_word(letters, includes):
        remaining = letters.copy()
        for inc in includes:
            if inc.upper() in remaining:
                remaining.remove(inc)
            else:
                return False

        return True
