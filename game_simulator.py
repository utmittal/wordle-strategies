import random
from enum import StrEnum
from wordle_dictionary import WordleDictionary
from pycharm_termcolor import colored, cprint


class State(StrEnum):
    blank = 'white'
    grey = 'light_grey'
    yellow = 'yellow'
    green = 'green'


class GameSimulator:
    def __init__(self):
        self.__secret_word = None
        self.__game_state = [[('_', State.blank)] * 5] * 6
        self.__turn = None
        self.__wd = None
        self.__game_won = None

    def _debug_start_game(self, puzzle_word, interactive=False):
        self.__secret_word = puzzle_word.upper()
        self.__wd = WordleDictionary()
        self.__turn = 0
        self.__game_won = False

        if interactive:
            self.__run_interactive_loop()

    def start_game(self, interactive=False):
        temp_wd = WordleDictionary()
        self._debug_start_game(temp_wd.get_random_puzzle(), interactive=interactive)

    def guess(self, guess):
        if self.__game_won or self.__turn > 5:
            raise Exception("Game is already over.")

        if not self.__valid_guess(guess):
            # This method is for computers. We expect computers to make valid guesses. So we can
            # just straight up raise an exception.
            raise ValueError("Invalid guess.")

        evaluated_row = self.__evaluate_guess(guess)
        self.__game_state[self.__turn] = evaluated_row
        self.__turn += 1

        self.__evaluate_win_state(guess)

        return self.__game_state

    def get_game_state(self):
        return self.__game_state

    def is_won(self):
        return self.__game_won

    def is_lost(self):
        if self.__turn > 5:
            return True
        else:
            return False

    def __valid_guess(self, guess, interactive=False):
        if len(guess) != 5:
            if interactive:
                cprint("Guess must be a 5 letter word.", 'red')
            return False

        if not self.__wd.contains(guess):
            if interactive:
                cprint("Invalid word.", 'red')
            return False

        return True

    def __evaluate_guess(self, guess):
        guess = guess.upper()
        evaluation = [()] * 5
        remaining_letters = list(self.__secret_word)

        # We need this double iteration to handle repeated letters in the words. The way wordle works is that if the
        # puzzle word has two of the same letters, say "tools", in the guess highlighting, priority is given to green
        # highlighting. If a letter is already highlighted in green, it must not be given a yellow highlight unless
        # there is a double of it in the puzzle word.
        for guess_letter, actual_letter, index in zip(guess, self.__secret_word, range(0, 5)):
            if guess_letter == actual_letter:
                tup = (guess_letter, State.green)
                remaining_letters.remove(guess_letter)
                evaluation[index] = tup

        for guess_letter, actual_letter, index in zip(guess, self.__secret_word, range(0, 5)):
            if guess_letter != actual_letter:
                if guess_letter in remaining_letters:
                    tup = (guess_letter, State.yellow)
                    remaining_letters.remove(guess_letter)
                else:
                    tup = (guess_letter, State.grey)

                evaluation[index] = tup

        return evaluation

    def __evaluate_win_state(self, guess):
        guess = guess.upper()
        if guess == self.__secret_word:
            self.__game_won = True

    def __show_board(self):
        print()
        for row in self.__game_state:
            coloured_row = [colored(e[0], color=e[1].value) for e in row]
            print("\t" + ""' '.join(coloured_row))
        print()

    def __run_interactive_loop(self):
        cprint("Starting Wordle!", 'blue')

        while self.__turn < 6:
            self.__show_board()

            guess_length = 0
            valid_guess = False
            guess = None
            while guess_length != 5 or valid_guess == False:
                guess = input("Guess: ")
                guess_length = len(guess)
                if guess_length != 5:
                    cprint("Guess must be a 5 letter word.", 'red')
                elif not self.__wd.contains(guess):
                    cprint("Invalid word.", 'red')
                else:
                    valid_guess = True

            evaluated_row = self.__evaluate_guess(guess)
            self.__game_state[self.__turn] = evaluated_row

            self.__evaluate_win_state(guess)
            if self.__game_won:
                self.__show_board()
                cprint("You won in " + str(self.__turn + 1) + " turns!", 'blue')
                return

            self.__turn += 1

        self.__show_board()
        cprint("You lost :( The word was " + self.__secret_word + ".", 'blue')
