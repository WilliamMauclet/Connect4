import os
import sys
import time

sys.path.insert(0, os.path.abspath('.'))

from hispida.bots.Bot import Bot
from hispida.grid.Grid import Grid
from hispida.utils.TimeFormat import format_time


def start():
    grid = Grid()
    print("\nWelcome to a new game of Connect 4\n")
    bot = _choose_opponent()
    print("To exit the game press Q + ENTER\n"
          "Please make the first move")

    id_index = 1
    grid.print_grid()
    while not grid.game_over():
        id_index = (id_index + 1) % 2
        _accept_move(grid, id_index, bot)
        grid.print_grid()

    print([HUMAN_PLAYER_ID, BOT_PLAYER_ID][id_index] + " won, congrats!\n")
    print("Replay:\n")
    print(grid.logs)


def _choose_opponent() -> Bot:
    print("Choose an opponent against whom to play:\n")

    inp = None
    accepted_inputs = ['', '-1', '0', '1', '2']
    while inp not in accepted_inputs:
        inp = input(
            "-1 for MinusOneOrderBot, "
            "0 for ZeroOrderBot, "
            "1 for FirstOrderBot, "
            "2 for MinmaxBot(alpha-beta) "
            "(last=default): ")
    if inp is "":
        inp = accepted_inputs[-1]
    if inp == '-1':
        print("\nThis game is against an opponent playing randomly.\n")
        from hispida.bots.MinusFirstOrderBot import MinusFirstOrderBot
        return MinusFirstOrderBot(BOT_PLAYER_ID)
    elif inp == '0':
        print("\nThis game is against an opponent playing randomly but avoiding simple traps.\n")
        from hispida.bots.ZeroOrderBot import ZeroOrderBot
        return ZeroOrderBot(BOT_PLAYER_ID)
    elif inp == '1':
        print("\nThis game is against an opponent playing randomly but avoiding (/to make) simple traps.\n")
        from hispida.bots.FirstOrderBot import FirstOrderBot
        return FirstOrderBot(BOT_PLAYER_ID)
    elif inp == '2':
        print("\nThis game is against an opponent using a minmax algorithm with alpha-beta pruning.\n")
        from hispida.bots.MinmaxBot import MinmaxBot
        bot = MinmaxBot(BOT_PLAYER_ID, depth=9, heuristic_bot=1, heuristic_opponent=-3)
        return bot
    else:
        raise Exception("Did not recognise bot id: '" + inp + "'")


def _accept_move(grid, id_index, bot):
    if id_index:
        timestamp = time.time()
        column = bot.choose_move(grid)
        print("Computing time: ", format_time(time.time() - timestamp))
    else:
        column = _accept_human_move(grid)

    print(["You", "Bot"][id_index] + " played column: " + str(column + 1))
    grid.add_pawn(column, [HUMAN_PLAYER_ID, BOT_PLAYER_ID][id_index])


def _accept_human_move(grid) -> int:
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    accepted_inputs = ['q', 'Q'] + [str(x + 1) for x in grid.get_free_columns()]
    while inp not in accepted_inputs:
        inp = input("Please give one of the following values: " + str(accepted_inputs) + "\n")

    if inp == 'q' or inp == 'Q':
        raise Exception("Game finished by player")
    else:
        return int(inp) - 1

# TODO
# change here if you want to get more messages.
import logging

logging.getLogger().setLevel(logging.CRITICAL)
# except Exception as exc:
# print(exc.__str__())

HUMAN_PLAYER_ID = 'H'
BOT_PLAYER_ID = 'B'

start()
