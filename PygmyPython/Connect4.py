from Grid import ColumnGrid
from Robots.MinusFirstOrderRobot import MinusFirstOrderRobot
from Robots.ZeroOrderRobot import ZeroOrderRobot

from PygmyPython.Robots.FirstOrderRobot import FirstOrderRobot

humanPlayerId = 'X'
robotPlayerId = 'O'

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
    acceptedInputs = ['', '-1', '0', '1']
    while inp not in acceptedInputs:
        inp = input("-1 for MinusOneOrderRobot, 0 for ZeroOrderRobot and 1 for FirstOrderRobot (last=default): ")
    if inp is "":
        inp = acceptedInputs[-1]
    if inp is '-1':
        print("\nThis game is against an opponent playing randomly.\n")
        return MinusFirstOrderRobot(robotPlayerId)
    elif inp is '0':
        print("\nThis game is against an opponent playing randomly but avoiding simple traps.\n")
        return ZeroOrderRobot(robotPlayerId)
    elif inp is '1':
        print("\nThis game is against an opponen playing randomly but avoiding (/to make) simple traps.\n")
        return FirstOrderRobot(robotPlayerId)
    else:
        raise Exception("Did not recognise robot id: '" + inp + "'")


def start():
    grid = ColumnGrid()

    print("\nWelcome to a new game of Connect 4\n")

    robot = choose_opponent()

    print("To exit the game press Q + ENTER\n")
    print("Please do the first move")

    # try:
    while grid.game_over() == -1:
        grid.print_grid()
        column = accept_human_move(grid)
        grid.add_pawn(column, humanPlayerId)

        if grid.game_over() != -1:
            break

        column = robot.choose_move(grid)
        grid.add_pawn(column, robotPlayerId)

    grid.print_grid()
    print("\nPlayer " + str(grid.game_over()) + " won, congrats!\n")


# except Exception as exc:
# print(exc.__str__())
start()
