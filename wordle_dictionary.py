import random


class WordleDictionary:
    def __init__(self):
        with open('database/words.txt', 'r') as f:
            lines = f.read().splitlines()
        self.__words = [w.strip().upper() for w in lines]

    def get_random_word(self):
        return random.choice(self.__words)

    def contains(self, word):
        if word.upper() in self.__words:
            return True
        else:
            return False
