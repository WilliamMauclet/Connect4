### DOING
---
### TODO
* Testing
    * Test match-off
* Even if MinmaxBot sees it's going to lose: don't play randomly, but a move that will make it lose as late as possible.
    * Also keep depth at turn of losing, so that the above can be known.
* Better handling of player ending game => exception should be handled

---
### IDEAS
* MinmaxBot: shuffle moves_scores? => makes it less re-playable! :(
* Create Game class with Grid and with 2 players(Bots or Bot/human) and resolve()
---
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
* 2017/08/29: In MatchOff: change "test" to "match"
* 2017/08/31: Using Bot.get_descriptor() in MatchOff
* 2017/08/31: Rework match-off to determine best bot. Final JSON output schema. Refactoring.
* 2017/09/01: Don't save matches one line at a time: extend match-off json.
* 2017/09/01: Delete JsonifierOfResults?
---
### ABANDONED IDEAS
* Bot accepts history of moves to machine learn
* First checks when choosing moves are make the bot play worse! => Don't do this ???? TODO
* Replace list(grid.get_free_columns()) with new function? Uses: 3 / 12 total usages => No
