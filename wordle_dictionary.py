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

    def contains(self, word):
        if word.upper() in self.__valid_guesses:
            return True
        else:
            return False

    def get_random(self):
        return random.choice(self.__valid_guesses)
