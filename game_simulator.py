import random
from enum import StrEnum
from wordle_dictionary import WordleDictionary
from termcolor import colored
import os

class State(StrEnum):
    blank = 'white'
    grey = 'grey'
    yellow = 'yellow'
    green = 'green'

class GameSimulator:
    def __init__(self):
        self.__secret_word = None
        self.__game_state = [[('_',State.yellow)]*5]*6

    def start_game(self):
        wd = WordleDictionary()
        self.__secret_word = wd.get_word()

    def show_board(self):
        # enables colours on windows terminals
        os.system('color')

        for row in self.__game_state:
            coloured_row = [colored(e[0],color=e[1].value,force_color=True) for e in row]
            print(' '.join(coloured_row))



gs = GameSimulator()
gs.start_game()
gs.show_board()
