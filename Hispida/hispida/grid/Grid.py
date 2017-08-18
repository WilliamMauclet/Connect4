from typing import Iterator, Optional


class Grid:
    WIDTH = 7
    HEIGHT = 6

    def __init__(self):
        self.columns = [[None for _ in range(self.HEIGHT)] for _ in range(self.WIDTH)]
        # self.columns = [ [None] * height] * width => CAUSES PROBLEMS!
        self.logs = []

    def get_empty_top_index(self, x: int) -> Optional[int]:
        for y in range(6):
            if self.columns[x][y] is None:
                return y
        return None  # TODO replace with other absent value?

    # TODO test OR replace with get_empty_top_index
    def get_filled_top_index(self, x: int) -> int:
        index = self.get_empty_top_index(x)
        if not index:
            return 5
        if index is 0:
            raise Exception("Column was empty!")
        else:
            return index

    def get_column(self, x: int) -> [str]:
        return self.columns[x]

    def get_free_columns(self):
        for x in range(7):
            if self._is_column_free(x):
                yield x

    def is_full(self) -> bool:
        for index_col, _ in enumerate(self.columns):
            if self._is_column_free(index_col):
                return False
        return True

    def add_pawn(self, x: int, player_id: str) -> None:
        self.logs.append((x, player_id))
        y = self.get_empty_top_index(x)
        self.columns[x][y] = player_id

    def add_pawn_history(self, moves: [int, str]) -> None:
        for move in moves:
            self.add_pawn(move[0], move[1])

    # TODO absent return type
    def game_over(self) -> str:
        for column in self.columns:
            if self._four_in_a_row(column) != -1:
                return self._four_in_a_row(column)
        for y in range(6):
            row = [self.columns[x][y] for x in range(7)]
            if self._four_in_a_row(row) != -1:
                return self._four_in_a_row(row)
        if self._check_all_diagonals_for_win() != -1:
            return self._check_all_diagonals_for_win()
        if self.is_full():
            return "exaequo"

        return -1

    def print_grid(self) -> None:
        print(self.get_state_string_representation())

    def get_state_string_representation(self) -> str:
        image = ''
        for x in range(15):
            image += '_'
        for y in range(5, -1, -1):
            image += '\n|'
            for x in range(7):
                if self.columns[x][y] is None:
                    image += '_|'
                else:
                    image += self.columns[x][y] + '|'
        image += '\n'
        return image

    def _is_column_free(self, x):
        return self.columns[x][-1] is None

    @staticmethod
    def _four_in_a_row(row):
        seq = 1
        prev = None
        for tile in row:
            if tile is None or tile != prev:
                seq = 1
            elif tile == prev:
                seq += 1

            if seq is 4:
                return tile
            prev = tile
        return -1

    def _get_right_up_diagonal(self, x, y):
        row = []
        while x <= 6 and y <= 5:
            row.append(self.columns[x][y])
            x += 1
            y += 1
        return row

    def _get_left_up_diagonal(self, x, y):
        row = []
        while x >= 0 and y <= 5:
            row.append(self.columns[x][y])
            x -= 1
            y += 1
        return row

    def _check_all_diagonals_for_win(self):
        for y in range(6):
            diagonals = (self._get_right_up_diagonal(0, y), self._get_left_up_diagonal(6, y))

            for diagonal in diagonals:
                if self._four_in_a_row(diagonal) != -1:
                    return self._four_in_a_row(diagonal)
        for x in range(7):
            diagonals = (self._get_left_up_diagonal(x, 0), self._get_right_up_diagonal(x, 0))

            for diagonal in diagonals:
                if self._four_in_a_row(diagonal) != -1:
                    return self._four_in_a_row(diagonal)
        return -1

    def clone_with_move(self, move: int, player_id: str) -> 'Grid':
        clone = self._clone()
        clone.add_pawn(move, player_id)
        return clone

    def clone_with_move_opponent(self, move: int, player_id: str) -> 'Grid':
        clone = self._clone()
        opponent_id = self._get_id_opponent(player_id)
        if opponent_id:
            clone.add_pawn(move, opponent_id)
        else:
            clone.add_pawn(move, 'random')
        return clone

    def _clone(self):
        clone = Grid()
        clone.columns = [[tile for tile in column] for column in self.columns]
        return clone

    def _get_id_opponent(self, player_id):
        for column in self.columns:
            for tile_id in column:
                if tile_id and tile_id != player_id:
                    return tile_id
        return ''

    def _get_tiles(self):
        for column in self.columns:
            for tile in column:
                yield tile

    def get_bordering_tiles(self, x_co: int, y_co: int) -> Iterator[str]:
        for y in range(-1, 2):
            for x in range(-1, 2):
                if 0 <= x_co + x < self.WIDTH and 0 <= y_co + y < self.HEIGHT:
                    yield self.columns[x_co + x][y_co + y]

    def get_nr_moves_left(self) -> int:
        return sum(self.columns[x].count(None) for x in self.get_free_columns())

    def get_last_move(self) -> (int, str):
        return self.logs[-1]
