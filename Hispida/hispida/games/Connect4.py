import os
import sys

sys.path.insert(0, os.path.abspath("."))

from Bot import Bot
from Grid import Grid


def accept_human_move(grid):
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    accepted_inputs = ['q', 'Q'] + [str(x + 1) for x in grid.get_free_columns()]
    while inp not in accepted_inputs:
        inp = input("Please give one of the following values: " + str(accepted_inputs) + "\n")

    if inp == 'q' or inp == 'Q':
        raise Exception("Game finished by player")
    else:
        return int(inp) - 1


def accept_human_move_prev(grid):
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    if inp is 'q':
        raise Exception("Game aborted")
    column = int(inp) - 1
    while not grid.is_column_free(column):
        inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
        if inp is 'q':
            raise Exception("Game aborted")
        column = int(inp) - 1
    return column


# noinspection PyCallingNonCallable
def choose_opponent() -> Bot:
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
        bot = MinmaxBot(BOT_PLAYER_ID, heuristic_bot=2, heuristic_opponent=1, depth=7)
        return bot
    else:
        raise Exception("Did not recognise bot id: '" + inp + "'")


def start():
    grid = Grid()
    print("\nWelcome to a new game of Connect 4\n")
    bot = choose_opponent()
    print("To exit the game press Q + ENTER\n")
    print("Please make the first move")

    id_index = 1
    grid.print_grid()
    while grid.game_over() == -1:
        id_index = (id_index + 1) % 2
        player_id = [HUMAN_PLAYER_ID, BOT_PLAYER_ID][id_index]
        accept_move(grid, player_id, bot)
        grid.print_grid()
        if grid.game_over() != -1:
            break

    print(get_player_tag_from_id(str(grid.game_over())) + " won, congrats!\n")


def accept_move(grid, player_id, bot):
    if player_id == HUMAN_PLAYER_ID:
        column = accept_human_move(grid)
    else:
        column = bot.choose_move(grid)
    print(get_player_tag_from_id(player_id) + " played column: " + str(column + 1))
    grid.add_pawn(column, player_id)


def get_player_tag_from_id(player_id):
    if player_id == HUMAN_PLAYER_ID:
        return "You"
    else:
        return "Bot"


# change here if you want to get more messages.
import logging

logging.getLogger().setLevel(logging.CRITICAL)
# except Exception as exc:
# print(exc.__str__())

HUMAN_PLAYER_ID = 'X'
BOT_PLAYER_ID = 'O'

start()
