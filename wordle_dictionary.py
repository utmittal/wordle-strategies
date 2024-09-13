import random
from game_simulator import TOTAL_LETTERS


def _parse_words_from_file(path):
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
        green_sets = [self.__letter_pos_index[g.upper()][greens[g]] for g in greens]
        if len(green_sets) == 0:
            valid_guesses_greens = self.__valid_guesses_set
        else:
            valid_guesses_greens = set.intersection(*green_sets)

        # all valid guesses that have an excludes letter in them
        if len(excludes) == 0:
            guesses_excludes = set()
        else:
            guesses_excludes = set.union(*[self.__letter_index[e.upper()] for e in excludes])

        # all valid guesses that have an includes letter in them
        if len(includes) == 0:
            guesses_includes = self.__valid_guesses_set
        else:
            guesses_includes = set.union(*[self.__letter_index[i.upper()] for i in includes])

        filtered_guesses = list((valid_guesses_greens.intersection(guesses_includes)).difference(guesses_excludes))

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
