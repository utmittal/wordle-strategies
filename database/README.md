Historically, Wordle had a list of valid guesses (`valid_guesses.txt`) and a separate list of words from which the
puzzles would be picked (`valid_puzzles.txt`).
This would allow words like "AAHED" to be used as a guess, but they would never be picked as the puzzle of the day. I.e.
the second list consisted of more common words.

NYT no longer uses this original list, though presumably the list of valid guesses remains accurate. For the purposes of
this code, we will use the list of valid puzzle words to pick our puzzle (and evaluate our solutions).

Source for valid words: https://gist.github.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04

Source for valid puzzles: https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee