import random

import wordle_dictionary as wd

def pretty_print_word(word):
    print(' '.join(word))

def choose_word(words):
    return random.choice(words)

def run_game():
    # load dictionary
    valid_words = wd.get_all_words()

    # choose the word the player will guess
    secret_word = choose_word(valid_words)

    # 