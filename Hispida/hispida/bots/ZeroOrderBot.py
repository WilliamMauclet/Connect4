import random

from Bot import Bot


class ZeroOrderBot(Bot):
    """This bot applies simple algorithms to see if it can avoid a four in a row.
    If not, it just plays randomly."""

    def choose_move(self, grid) -> int:
        if self._check_if_immediate_win_possible(grid):
            return self._check_if_immediate_win_possible(grid)['column']
        else:
            return random.choice(grid.get_free_columns())

    def _check_if_immediate_win_possible(self, grid) -> dict:
        for x in grid.get_free_columns():
            y = self._find_top_empty_tile(grid.columns[x])
            if self._check_triplet_below(grid, x, y):
                return self._check_triplet_below(grid, x, y)
            if self._check_adjacents(grid, x, y):
                return self._check_adjacents(grid, x, y)
            if self._check_diagonals(grid, x, y):
                return self._check_diagonals(grid, x, y)
        return {}

    @staticmethod
    def _find_top_empty_tile(column):
        y = 5
        while column[y] is None and y >= 0:
            y -= 1
        return y + 1

    @staticmethod
    def _check_response(column, player) -> dict:
        return {'column': column, 'player': player}

    def _check_triplet_below(self, grid, x, y) -> dict:
        column = grid.columns[x]
        if y < 3:
            return {}
        if column[y - 1] == column[y - 2] == column[y - 3] is not None:
            return self._check_response(x, column[y - 1])
        return {}

    def _check_adjacents(self, grid, x, y) -> dict:
        if self._check_adjacent_triplet(grid, x, y):
            self._log("FOUND 3-0 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return self._check_adjacent_triplet(grid, x, y)
        if self._check_adjacent_double_and_single(grid, x, y):
            self._log("FOUND 2-1 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return self._check_adjacent_double_and_single(grid, x, y)
        return {}

    def _check_adjacent_triplet(self, grid, x, y) -> dict:
        if x <= 3 and grid.columns[x + 1][y] == grid.columns[x + 2][y] == grid.columns[x + 3][y] is not None:
            return self._check_response(x, grid.columns[x + 1][y])
        if x >= 3 and grid.columns[x - 1][y] == grid.columns[x - 2][y] == grid.columns[x - 3][y] is not None:
            return self._check_response(x, grid.columns[x - 1][y])
        return {}

    def _check_adjacent_double_and_single(self, grid, x, y) -> dict:
        if 1 <= x <= 4 and grid.columns[x - 1][y] == grid.columns[x + 1][y] == grid.columns[x + 2][y] is not None:
            return self._check_response(x, grid.columns[x - 1][y])
        if 2 <= x <= 5 and grid.columns[x - 2][y] == grid.columns[x - 1][y] == grid.columns[x + 1][y] is not None:
            return self._check_response(x, grid.columns[x - 2][y])
        return {}

    def _check_diagonals(self, grid, x, y) -> dict:
        if self._check_diagonal_triplet(grid, x, y):
            self._log("FOUND 3-0 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return self._check_diagonal_triplet(grid, x, y)
        if self._check_diagonal_double_and_single(grid, x, y):
            self._log("FOUND 2-1 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
            return self._check_diagonal_double_and_single(grid, x, y)
        return {}

    def _check_diagonal_triplet(self, grid, x, y) -> dict:
        # look up
        if y <= 2:
            # look right
            if x <= 3 and grid.columns[x + 1][y + 1] == grid.columns[x + 2][y + 2] == grid.columns[x + 3][
                        y + 3] is not None:
                return self._check_response(x, grid.columns[x + 1][y + 1])
            # look left
            if x >= 3 and grid.columns[x - 1][y + 1] == grid.columns[x - 2][y + 2] == grid.columns[x - 3][
                        y + 3] is not None:
                return self._check_response(x, grid.columns[x - 1][y + 1])
        if y >= 3:
            if x <= 3 and grid.columns[x + 1][y - 1] == grid.columns[x + 2][y - 2] == grid.columns[x + 3][
                        y - 3] is not None:
                return self._check_response(x, grid.columns[x + 1][y - 1])
            if x >= 3 and grid.columns[x - 1][y - 1] == grid.columns[x - 2][y - 2] == grid.columns[x - 3][
                        y - 3] is not None:
                return self._check_response(x, grid.columns[x - 1][y - 1])
            return {}

    def _check_diagonal_double_and_single(self, grid, x, y) -> dict:
        # look up (= long tail to the right)
        # look left
        if 0 < y <= 3 and 2 <= x <= 5:
            if grid.columns[x - 1][y + 1] == grid.columns[x - 2][y + 2] == grid.columns[x + 1][y - 1] is not None:
                return self._check_response(x, grid.columns[x - 1][y + 1])
                # look right
        if 0 < y <= 3 and 1 <= x <= 4:
            if grid.columns[x - 1][y - 1] == grid.columns[x + 1][y + 1] == grid.columns[x + 2][y + 2] is not None:
                return self._check_response(x, grid.columns[x - 1][y - 1])
                # look down
                # look left
        if 2 <= y <= 4 and 2 <= x <= 5:
            if grid.columns[x - 2][y - 2] == grid.columns[x - 1][y - 1] == grid.columns[x + 1][y + 1] is not None:
                return self._check_response(x, grid.columns[x - 2][y - 2])
                # look right
        if 2 <= y <= 4 and 1 <= x <= 4:
            if grid.columns[x - 1][y + 1] == grid.columns[x + 1][y - 1] == grid.columns[x + 2][y - 2] is not None:
                return self._check_response(x, grid.columns[x - 1][y + 1])
            return {}
