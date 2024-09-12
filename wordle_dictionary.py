import random


def _parse_words_from_file(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return [w.strip().upper() for w in lines]


class WordleDictionary:
    def __init__(self):
        self.__valid_guesses = _parse_words_from_file('database/valid_guesses.txt')
        self.__valid_puzzles = _parse_words_from_file('database/valid_puzzles.txt')

        # create index of words containing a specific letter
        self.__guesses_index = {}
        for g in self.__valid_guesses:
            letters = list(g)
            for l in letters:
                if l in self.__guesses_index:
                    self.__guesses_index[l].add(g)
                else:
                    self.__guesses_index[l] = {g}

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

        # remove all words which have letters from the excludes list in them
        valid_minus_excludes = set(self.__valid_guesses).difference(
            *[self.__guesses_index[e.upper()] for e in excludes])

        filtered_guesses = []
        for word in valid_minus_excludes:
            letters = list(word.upper())

            if self.__eval_word(letters, greens, includes):
                filtered_guesses.append(word)

        return filtered_guesses

    @staticmethod
    def __eval_word(letters, green_dic, includes):
        remaining = letters.copy()
        for i in green_dic:
            if green_dic[i].upper() != letters[i]:
                return False
            else:
                remaining.remove(green_dic[i])

        for inc in includes:
            if inc.upper() in remaining:
                remaining.remove(inc)
            else:
                return False

        return True
