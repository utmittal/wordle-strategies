import random


def _parse_words_from_file(path):
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    return [w.strip().upper() for w in lines]


class WordleDictionary:
    def __init__(self):
        self.__valid_guesses = _parse_words_from_file('database/valid_guesses.txt')
        self.__valid_puzzles = _parse_words_from_file('database/valid_puzzles.txt')

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

        filtered_guesses = []
        for word in self.__valid_guesses:
            letters = list(word.upper())

            if self.__eval_word(letters, greens, includes, excludes):
                filtered_guesses.append(word)

        return filtered_guesses

    @staticmethod
    def __eval_word(letters, green_dic, includes, excludes):
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

        for exc in excludes:
            if exc.upper() in remaining:
                return False

        return True
