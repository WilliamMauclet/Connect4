import sys, os

sys.path.insert(0, os.path.abspath("."))

from Grid.Grid import ColumnGrid
from Robots.MinusFirstOrderRobot import MinusFirstOrderRobot
from Robots.ZeroOrderRobot import ZeroOrderRobot
from Robots.FirstOrderRobot import FirstOrderRobot
from Robots.MinmaxRobot import MinmaxRobot


def accept_human_move(grid):
    inp = input("Available columns: " + str([x + 1 for x in grid.get_free_columns()]) + "\n")
    acceptedInputs = ['q', 'Q'] + [str(x + 1) for x in grid.get_free_columns()]
    while inp not in acceptedInputs:
        inp = input("Please give one of the following values: " + str(acceptedInputs) + "\n")

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


def choose_opponent():
    print("Choose an opponent against whom to play:\n")
    inp = None
    acceptedInputs = ['', '-1', '0', '1', '2']
    while inp not in acceptedInputs:
        inp = input(
            "-1 for MinusOneOrderRobot, 0 for ZeroOrderRobot, 1 for FirstOrderRobot and 2 for ManyOrderRobot (last=default): ")
    if inp is "":
        inp = acceptedInputs[-1]
    if inp is '-1':
        print("\nThis game is against an opponent playing randomly.\n")
        return MinusFirstOrderRobot(ROBOT_PLAYER_ID)
    elif inp is '0':
        print("\nThis game is against an opponent playing randomly but avoiding simple traps.\n")
        return ZeroOrderRobot(ROBOT_PLAYER_ID)
    elif inp is '1':
        print("\nThis game is against an opponent playing randomly but avoiding (/to make) simple traps.\n")
        return FirstOrderRobot(ROBOT_PLAYER_ID)
    elif inp is '2':
        print("\nThis game is against an opponent using a minmax algorithm.\n")
        return MinmaxRobot(ROBOT_PLAYER_ID)
    else:
        raise Exception("Did not recognise robot id: '" + inp + "'")


def start():
    grid = ColumnGrid()

    print("\nWelcome to a new game of Connect 4\n")

    robot = choose_opponent()

    print("To exit the game press Q + ENTER\n")
    print("Please do the first move")

    while grid.game_over() == -1:
        grid.print_grid()
        column = accept_human_move(grid)
        grid.add_pawn(column, HUMAN_PLAYER_ID)

        if grid.game_over() != -1:
            break

        column = robot.choose_move(grid)
        grid.add_pawn(column, ROBOT_PLAYER_ID)

    grid.print_grid()
    print("\nPlayer " + str(grid.game_over()) + " won, congrats!\n")


# change here if you want to get more messages.
import logging

logging.getLogger().setLevel(logging.CRITICAL)
# except Exception as exc:
# print(exc.__str__())

HUMAN_PLAYER_ID = 'X'
ROBOT_PLAYER_ID = 'O'

start()
