import sys

from MatchOff import match_off
from MinmaxBot import MinmaxBot

MATCH_OFF_FOLDER = "../../docs/match_offs/{}"


def _ultimate_match_off():
    """Define here the bots you want to match against each other. Use then the function match_off."""
    bots, file_path = _competing_bots(), MATCH_OFF_FOLDER.format("match_off_1.txt")
    match_off(bots, file_path=file_path, nr_of_games=2)
    sys.stdout.write("\n\nRound-robin match-off done.")


def _competing_bots():
    bots = []
    for i in range(-2, 0):
        for j in range(-2, 0):
            bots.append(MinmaxBot('Z', heuristic_bot=i, heuristic_opponent=j))
    return bots


_ultimate_match_off()
