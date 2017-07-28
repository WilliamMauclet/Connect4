# Connect4: Hispida
Connect 4 in python for AI experiment. Using a minmax algorithm.

### START
To play against one of the bots, run hispida/games/Connect4.py

If you want to automatically let bots play a chosen number of times against each other,
run Games/MultiGame.py

### DOING

### TODO
* Complete type hinting for all non-protected methods.
    * Re-work absent return types in grid: game_over, _four_in_a_row
* Testing
* MinmaxBot doesn't work.
    * Make test for game with moves 4, 3, 5 & 6 (Bot must always choose column with lowest index)
    * alpha-beta function in MinmaxBot must return predicted history of moves.
* Rework match-off module to determine best bot (configuration).
* Delete JsonifierOfResults?
* Better handling of player ending game => exception should be handled

### IDEAS
* Give Bots integers as ids instead of just 'X' and 'O'
* Create Game class with Grid and with 2 players(Bots or Bot/human) and resolve()

### DONE
* 2017/03/05: Bots.
* 2017/03/05: Use logger.
* 2017/03/05: Refactoring: push down method implementations.
* 2017/03/17: Minmax: Trivial case where a (simple) heuristic is used to evaluate a grid-situation.
* 2017/03/17: Minmax: Recursive case, where child branches are merged.
* 2017/03/22: Jsonfication.
* 2017/04/18: Minmax: alpha-beta pruning.
* 2017/03/17: Game keeps history of moves.
* 2017/07/21: Renamed Bots to Bots.
* 2017/07/21: Removed Bot.get_id_opponent(): No more assumption that only player ids "X" and "O" are used!
* 2017/07/21: Renamed MultiGame to Match-off
* 2017/07/22: Underscored private function names in classes and modules.
* 2017/07/27: Re-factoring Grid
* 2017/07/28: Replay possibility (for debugging)
* 2017/07/28: Type hinting for non-protected functions in Grid

### ABANDONED IDEAS
* Bot accepts history of moves to machine learn
* First checks when choosing moves are make the bot play worse! => Don't do this ???? TODO
* Replace list(grid.get_free_columns()) with new function? Uses: 3 / 12 total usages => No
