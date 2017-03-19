import random
from Robots.ZeroOrderRobot import ZeroOrderRobot


class FirstOrderRobot(ZeroOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
    Except for that, it just plays randomly."""

    def does_move_help_opponent(self, grid, x) -> bool:
        new_grid = grid.clone_with_move(x, self.robot_id)
        return self.check_if_immediate_win_possible(new_grid) \
               and self.check_if_immediate_win_possible(new_grid)['player'] == self.get_id_opponent()

    def choose_move_that_does_not_help_opponent(self, grid) -> int:
        freeColumns = grid.get_free_columns()
        dangerousColumns = []
        for x in freeColumns:
            if self.does_move_help_opponent(grid, x):
                dangerousColumns.append(x)
        if len(freeColumns) == len(dangerousColumns):
            self.log("GAME IS LOST WHATEVER MOVE I MAKE")
            return random.choice(freeColumns)
        return random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        if self.check_if_immediate_win_possible(grid):
            return self.check_if_immediate_win_possible(grid)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
