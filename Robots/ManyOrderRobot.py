import random

from Robots.FirstOrderRobot import FirstOrderRobot


class ManyOrderRobot(FirstOrderRobot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create a future win possibility for the opponent.
    Except for that, it just plays randomly."""

    def choose_move_that_does_not_help_opponent(self, grid):
        """TODO Should give score to every column > choose (randomly from) column(s) with highest score"""
        freeColumns = grid.get_free_columns()
        dangerousColumns = []

        for x in freeColumns:
            column = self.evaluate_column_does_not_help_opponent(grid, x)
            if column is not None:
                dangerousColumns.append(column)

        if len(freeColumns) == len(dangerousColumns):
            return random.choice(freeColumns)
        else:
            return random.choice([i for i in freeColumns if i not in dangerousColumns])

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_columns(grid, freeColumns) != -1:
            return self.check_columns(grid, freeColumns)['column']
        else:
            return self.choose_move_that_does_not_help_opponent(grid)
