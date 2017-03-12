import random
from Robots.ZeroOrderRobot import ZeroOrderRobot


class FirstOrderRobot(ZeroOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
    Except for that, it just plays randomly."""

    def does_move_help_opponent(self, grid, x):
        y = self.find_top_empty(grid.columns[x])
        if y == 5:
            return False
        y += 1
        if self.check_adjacents(grid, x, y) != -1 and self.check_adjacents(grid, x, y)['player'] == self.get_id_opponent():
            self.log("AVOIDING TO CREATE ADJACENT TRAP AT (" + str(x) + "," + str(y) + ")")
            return True
        elif self.check_diagonals(grid, x, y) != -1 and self.check_diagonals(grid, x, y) == self.get_id_opponent():
            self.log("AVOIDING TO CREATE DIAGONAL TRAP AT (" + str(x) + "," + str(y) + ")")
            return True
        return False

    def choose_move_that_does_not_help_opponent(self, grid):
        freeColumns = grid.get_free_columns()
        dangerousColumns = []
        for x in freeColumns:
            if self.does_move_help_opponent(grid,x):
                dangerousColumns.append(x)
        if len(freeColumns) == len(dangerousColumns):
            self.log("GAME IS LOST WHATEVER MOVE I MAKE")
            return random.choice(freeColumns)
        return random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_if_immediate_win_possible(grid, freeColumns) != -1:
            return self.check_if_immediate_win_possible(grid, freeColumns)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
