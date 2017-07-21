# Connect4: Hispida
Connect 4 in python for AI experiment. Using a minmax algorithm.

### START
To play against one of the bots, run hispida/games/Connect4.py

If you want to automatically let bots play a chosen number of times against each other,
run Games/MultiGame.py

### DOING

### TODO
* Underscore private function names in classes.
* Big match-off to determine best bot (configuration)
* Rework JsonifierOfResults.
* Better handling of player ending game => exception should be handled
* Replay possibility (for debugging) OR alternatively give grid run_test configuration

### TODO PREVIOUSLY
* Bot accepts history of moves to machine learn
* First checks when choosing moves are make the bot play worse! => remove

### IDEAS
* Rename MultiGame to Match-off
* Give Bots integers as ideas instead of just 'X' and 'O'
* Create Game class with Grid and with 2 players(Bots or Bot/human) and resolve()


### DONE
* Bots.
* Use logger.
* Refactoring: push down method implementations.
* Minmax: Trivial case where a (simple) heuristic is used to evaluate a grid-situation.
* Minmax: Recursive case, where child branches are merged.
* Jsonfication.
* Minmax: alpha-beta pruning.
* Game keeps history of moves.
* 2017/07/21: Rename Bots to Bots.
* 2017/07/21: Removed Bot.get_id_opponent(): No more assumption that only player ids "X" and "O" are used!
