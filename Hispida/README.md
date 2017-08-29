# Connect4: Hispida
Connect 4 in python for AI experiment. Using a minmax algorithm.

### START
To play against one of the bots, run hispida/games/Connect4.py

If you want to automatically let bots play a chosen number of times against each other,
run Games/MultiGame.py

### MATCH-OFF
The match-off is a match-off between all the bots present in this project.

## Structure
The hierarchy of a match-off is the following:

MATCH-OFF   = Lots of Bots against one another in a round-robin tournament
            = nr_bots*(nr_bots - 1)/2 matches
MATCH       = 2 Bots facing off against each other
            = default 30 games
GAME        = 1 game
            = max 42 moves

## Output
The output of the match-off is a json with the following structure:

match-off
|- [end_scores]
|- [bots_full_description]
|- winner
|- [matches]
	|- time
	|- winner
	|- [end_scores]
	|- [games]
		|- winner
		|- grid_end_configuration

### CHECKLIST/TODO
To see what has been done and still needs to be done (the TODO list), see the Checklist.md.
