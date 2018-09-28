import sys

from hispida.bots.FirstOrderBot import FirstOrderBot
from MatchOff import match_off
from hispida.bots.MinmaxBot import MinmaxBot

import sys
sys.path.append('../.') 

MATCH_OFF_FOLDER = "../../docs/match_offs/{}"


def _ultimate_match_off():
    """Define here the bots you want to match against each other. Use then the function match_off."""
    bots, file_path = _competing_bots(), MATCH_OFF_FOLDER.format("matches_{}.json")
    match_off(bots, file_path=file_path, test_number=5, nr_of_games=10)
    sys.stdout.write("\n\nRound-robin match-off done.")


# "MinmaxBot:5/20/-20/0/1/-3": 52,
# "MinmaxBot:5/20/-20/0/3/-3": 47

def _competing_bots():
    bots = [FirstOrderBot('Z')]
    for win in range(1, 4):
        for lose in range(1, 4):
            bots.append(MinmaxBot('Z', win_score=win*5, lose_score=lose*-5))

    return bots


_ultimate_match_off()
