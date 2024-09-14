from enum import StrEnum
from dataclasses import dataclass

from pycharm_termcolor import colored, cprint

TOTAL_LETTERS = 5
TOTAL_TURNS = 6


class LetterState(StrEnum):
    blank = 'white'
    grey = 'light_grey'
    yellow = 'yellow'
    green = 'green'


@dataclass(frozen=True)
class GameLetter:
    letter: str = '_'
    color: LetterState = LetterState.blank


class GameState:
    def __init__(self):
        self.__game_state = [[GameLetter() for _ in range(TOTAL_LETTERS)] for _ in range(TOTAL_TURNS)]
        self.__latest_row_index = -1
        self.__iter_counter = None

    def __iter__(self):
        self.__iter_counter = -1
        return self

    def __next__(self):
        self.__iter_counter += 1
        if self.__iter_counter < TOTAL_TURNS:
            return self.__game_state[self.__iter_counter]
        else:
            raise StopIteration

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__game_state[index.start: index.stop: index.step]
        else:
            return self.__game_state[index]

    def get_last_turn(self) -> list[GameLetter]:
        return self.__game_state[self.__latest_row_index]

    def _add_turn(self, row: list[GameLetter]) -> None:
        """
        Auto increments turn number. This method is mostly meant for the game simulator class.
        """
        self.__latest_row_index += 1
        self.__game_state[self.__latest_row_index] = row


class GameSimulator:
    def __init__(self, wd):
        self.__secret_word = None
        self.__game_state = GameState()
        self.__turn = None
        self.__wd = wd
        self.__game_won = None

    def __reset_game(self):
        self.__secret_word = None
        self.__game_state = GameState()
        self.__turn = 0
        self.__game_won = False

    def start_game_with_puzzle(self, puzzle_word: str) -> GameState:
        self.__reset_game()
        self.__secret_word = puzzle_word.upper()

        return self.get_game_state()

    def start_game(self) -> GameState:
        return self.start_game_with_puzzle(self.__wd.get_random_puzzle())

    def start_interactive_game(self) -> None:
        self.__reset_game()
        self.__secret_word = self.__wd.get_random_puzzle().upper()
        self.__run_interactive_loop()

    def guess(self, guess: str) -> GameState:
        if self.__game_won or self.__turn > 5:
            raise Exception("Game is already over.")

        if not self.__valid_guess(guess):
            # This method is for computers. We expect computers to make valid guesses. So we can
            # just straight up raise an exception.
            raise ValueError("Invalid guess.")

        evaluated_row = self.__evaluate_guess(guess)
        self.__game_state._add_turn(evaluated_row)
        self.__turn += 1

        self.__evaluate_win_state(guess)

        return self.__game_state

    def get_game_state(self) -> GameState:
        return self.__game_state

    def get_turn(self) -> int:
        # because we increment at end of each turn, this represents the current turn number
        return self.__turn

    def is_won(self) -> bool:
        return self.__game_won

    def is_lost(self) -> bool:
        if self.__turn > 5 and self.__game_won != True:
            return True
        else:
            return False

    def __valid_guess(self, guess: str, interactive: bool = False) -> bool:
        if len(guess) != 5:
            if interactive:
                cprint("Guess must be a 5 letter word.", 'red')
            return False

        if not self.__wd.contains(guess):
            if interactive:
                cprint("Invalid word.", 'red')
            return False

        return True

    def __evaluate_guess(self, guess: str) -> list[GameLetter]:
        guess = guess.upper()
        evaluation = [GameLetter() for _ in range(TOTAL_LETTERS)]
        remaining_letters = list(self.__secret_word)

        # We need this double iteration to handle repeated letters in the words. The way wordle works is that if the
        # puzzle word has two of the same letters, say "tools", in the guess highlighting, priority is given to green
        # highlighting. If a letter is already highlighted in green, it must not be given a yellow highlight unless
        # there is a double of it in the puzzle word.
        for guess_letter, actual_letter, index in zip(guess, self.__secret_word, range(5)):
            if guess_letter == actual_letter:
                game_letter = GameLetter(guess_letter, LetterState.green)
                remaining_letters.remove(guess_letter)
                evaluation[index] = game_letter

        for guess_letter, actual_letter, index in zip(guess, self.__secret_word, range(0, 5)):
            if guess_letter != actual_letter:
                if guess_letter in remaining_letters:
                    game_letter = GameLetter(guess_letter, LetterState.yellow)
                    remaining_letters.remove(guess_letter)
                else:
                    game_letter = GameLetter(guess_letter, LetterState.grey)

                evaluation[index] = game_letter

        return evaluation

    def __evaluate_win_state(self, guess: str) -> bool:
        guess = guess.upper()
        if guess == self.__secret_word:
            self.__game_won = True

    def __show_board(self) -> None:
        print()
        for row in self.__game_state:
            coloured_row = [colored(gl.letter, color=gl.color.value) for gl in row]
            print("\t" + ""' '.join(coloured_row))
        print()

    def __run_interactive_loop(self) -> None:
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
            self.__game_state._add_turn(evaluated_row)

            self.__evaluate_win_state(guess)
            if self.__game_won:
                self.__show_board()
                cprint("You won in " + str(self.__turn + 1) + " turns!", 'blue')
                return

            self.__turn += 1

        self.__show_board()
        cprint("You lost :( The word was " + self.__secret_word + ".", 'blue')

    def _debug_get_puzzle_word(self) -> str:
        return self.__secret_word

    def _debug_print_board(self) -> None:
        self.__show_board()
