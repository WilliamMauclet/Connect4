import random
from Hispida.Robots.ZeroOrderRobot import ZeroOrderRobot


class FirstOrderRobot(ZeroOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
    Except for that, it just plays randomly."""

    def evaluate_column_does_not_help_opponent(self, grid, x):
        y = self.find_top_empty(grid.columns[x])
        if y == 5:
            return None
        y += 1
        if self.check_adjacents(grid, x, y) != -1 and self.check_adjacents(grid, x, y)['player'] != self.robotId:
            self.log("AVOIDING TO CREATE ADJACENT TRAP AT (" + str(x) + "," + str(y) + ")")
            return x
        elif self.check_diagonals(grid, x, y) != -1 and self.check_diagonals(grid, x, y) != self.robotId:
            self.log("AVOIDING TO CREATE DIAGONAL TRAP AT (" + str(x) + "," + str(y) + ")")
            return x

    def choose_move_that_does_not_help_opponent(self, grid):
        freeColumns = grid.get_free_columns()
        dangerousColumns = []
        for x in freeColumns:
            column = self.evaluate_column_does_not_help_opponent(grid, x)
            if column is not None:
                dangerousColumns.append(column)
        if len(freeColumns) == len(dangerousColumns):
            return random.choice(freeColumns)
        return random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_columns(grid, freeColumns) != -1:
            return self.check_columns(grid, freeColumns)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
