### DOING
* Use short_name()
    * Method in bots, gives full config of bot
    * Use it in MatchOff
    * Only detail full config in highest level json.
* Rework match-off module to determine best bot (configuration).
    * Schema of final json output
    * Don't save matches one line at a time: extend match-off json
    * merge _calc_match_off_end_scores() and _calc_match_end_scores()

### TODO
* Testing
* Even if MinmaxBot sees it's going to lose: don't play randomly, but a move that will make it lose as late as possible.
    * Also keep depth at turn of losing, so that the above can be known.
* Delete JsonifierOfResults?
* Better handling of player ending game => exception should be handled
* MinmaxBot: shuffle moves_scores? => makes it less re-playable! :(

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
* 2017/08/20: MinmaxBot doesn't work. => It was.
* 2017/08/20: MinmaxBot builds a minmax tree.
* 2017/08/22: Refactor MinmaxBot.
* 2017/08/22: Complete type hinting for return types in grid: game_over, \_four_in_a_row
* 2017/08$/29: In MatchOff: change "test" to "match"

### ABANDONED IDEAS
* Bot accepts history of moves to machine learn
* First checks when choosing moves are make the bot play worse! => Don't do this ???? TODO
* Replace list(grid.get_free_columns()) with new function? Uses: 3 / 12 total usages => No