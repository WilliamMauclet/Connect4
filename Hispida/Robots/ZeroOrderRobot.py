import random
from Robots.Robot import Robot


class ZeroOrderRobot(Robot):
    """This robot DOES NOT LEARN.
    It applies simple algorithms to see if it can avoid a four in a row.
    Except for that, it
    just plays randomly."""

    def find_top_empty(self, column):
        y = 5
        while column[y] is None and y >= 0:
            y -= 1
        return y + 1

    def has_triplet_below(self, column, y):
        if y < 3:
            return False
        if column[y - 1] == column[y - 2] == column[y - 3] is not None:
            return column[y - 1]
        return False

    def has_adjacent_triplet(self, grid, x, y):
        if x <= 3 and grid.columns[x + 1][y] == grid.columns[x + 2][y] == grid.columns[x + 3][y] is not None:
            return grid.columns[x + 1][y]
        if x >= 3 and grid.columns[x - 1][y] == grid.columns[x - 2][y] == grid.columns[x - 3][y] is not None:
            return grid.columns[x - 1][y]
        return False

    def has_adjacent_double_and_single(self, grid, x, y):
        if 1 <= x <= 4 and grid.columns[x - 1][y] == grid.columns[x + 1][y] == grid.columns[x + 2][y] is not None:
            return grid.columns[x - 1][y]
        if 2 <= x <= 5 and grid.columns[x - 2][y] == grid.columns[x - 1][y] == grid.columns[x + 1][y] is not None:
            return grid.columns[x - 2][y]
        return False

    def has_diagonal_triplet(self, grid, x, y):
        # look up
        if y <= 2:
            # look right
            if x <= 3 and grid.columns[x + 1][y + 1] == grid.columns[x + 2][y + 2] == grid.columns[x + 3][
                        y + 3] is not None:
                return grid.columns[x + 1][y + 1]
            # look left
            if x >= 3 and grid.columns[x - 1][y + 1] == grid.columns[x - 2][y + 2] == grid.columns[x - 3][
                        y + 3] is not None:
                return grid.columns[x - 1][y + 1]
        if y >= 3:
            if x <= 3 and grid.columns[x + 1][y - 1] == grid.columns[x + 2][y - 2] == grid.columns[x + 3][
                        y - 3] is not None:
                return grid.columns[x + 1][y - 1]
            if x >= 3 and grid.columns[x - 1][y - 1] == grid.columns[x - 2][y - 2] == grid.columns[x - 3][
                        y - 3] is not None:
                return grid.columns[x - 1][y - 1]
        return False

    def has_diagonal_double_and_single(self, grid, x, y):
        # look up (= long tail to the right)
        # look left
        if 0 < y <= 3 and 2 <= x <= 5:
            if grid.columns[x - 1][y + 1] == grid.columns[x - 2][y + 2] == grid.columns[x + 1][y - 1] is not None:
                return grid.columns[x - 1][y + 1]
                # look right
        if 0 < y <= 3 and 1 <= x <= 4:
            if grid.columns[x - 1][y + 1] == grid.columns[x + 1][y + 1] == grid.columns[x + 2][y + 2] is not None:
                return grid.columns[x - 1][y + 1]
                # look down
                # look left
        if 2 <= y <= 4 and 2 <= x <= 5:
            if grid.columns[x - 2][y - 2] == grid.columns[x - 1][y - 1] == grid.columns[x + 1][y + 1] is not None:
                return grid.columns[x - 2][y - 2]
                # look right
        if 2 <= y <= 4 and 1 <= x <= 4:
            if grid.columns[x - 1][y + 1] == grid.columns[x + 1][y - 1] == grid.columns[x + 2][y - 2] is not None:
                return grid.columns[x - 1][y + 1]
        return False

    def check_adjacents(self, grid, x, y):
        if self.has_adjacent_triplet(grid, x, y):
            self.log("FOUND 3-0 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return {'column': x, 'player': self.has_adjacent_triplet(grid, x, y)}
        if self.has_adjacent_double_and_single(grid, x, y):
            self.log("FOUND 2-1 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return {'column': x, 'player': self.has_adjacent_double_and_single(grid, x, y)}
        return -1

    def check_diagonals(self, grid, x, y):
        if self.has_diagonal_triplet(grid, x, y):
            self.log("FOUND 3-0 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return {'column': x, 'player': self.has_diagonal_triplet(grid, x, y)}
        if self.has_diagonal_double_and_single(grid, x, y):
            self.log("FOUND 2-1 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return {'column': x, 'player': self.has_diagonal_double_and_single(grid, x, y)}
        return -1

    def check_columns(self, grid, freeColumns):
        for x in freeColumns:
            y = self.find_top_empty(grid.columns[x])
            if self.has_triplet_below(grid.columns[x], y):
                return {'column': x, 'player': self.has_triplet_below(grid.columns[x], y)}
            if self.check_adjacents(grid, x, y) != -1:
                return self.check_adjacents(grid, x, y)
            if self.check_diagonals(grid, x, y) != -1:
                return self.check_diagonals(grid, x, y)
        return -1

    def choose_move(self, grid):
        freeColumns = grid.get_free_columns()
        if self.check_columns(grid, freeColumns) != -1:
            return self.check_columns(grid, freeColumns)['column']
        else:
            return random.choice(freeColumns)
