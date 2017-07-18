class Grid:
    WIDTH = 7
    HEIGHT = 6

    def __init__(self):
        self.columns = [[None for i in range(self.HEIGHT)] for j in range(self.WIDTH)]
        # self.columns = [ [None] * self.height] * self.width => CAUSES PROBLEMS!!!!!
        self.logs = []
        # TODO add timestamps to logs + first log records creation time?

    def get_empty_top_index(self, x):
        for y in range(6):
            if self.columns[x][y] is None:
                return y
        return None

    def get_filled_top_index(self, x):
        if self.columns[x][0] is None:
            raise Exception("Column was empty?")
        for y in range(6):
            if self.columns[x][y] is None:
                return y - 1
        return 5

    def get_column(self, x):
        return self.columns[x]

    def get_free_columns(self):
        return [x for x in range(7) if self.is_column_free(x)]

    def is_column_free(self, x):
        return self.columns[x][-1] is None

    def add_pawn(self, x, player_id):
        self.logs.append((x, player_id))
        y = self.get_empty_top_index(x)
        self.columns[x][y] = player_id

    def check_consistency(self):
        # assert len(self.columns) is 7, str(len(self.columbs) + " many columns found O.o"
        # nrPawnsDict = {None:0,PLAYER_ID_1:0,PLAYER_ID_2:0}
        for column in self.columns:
            assert len(column) is 6, "Column " + str(column) + " has " + str(len(column)) + " tiles! " + str(column)

    @staticmethod
    def four_in_a_row(row):
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

    def get_right_up_diagonal(self, x, y):
        row = []
        while x <= 6 and y <= 5:
            row.append(self.columns[x][y])
            x += 1
            y += 1
        return row

    def get_left_up_diagonal(self, x, y):
        row = []
        while x >= 0 and y <= 5:
            row.append(self.columns[x][y])
            x -= 1
            y += 1
        return row

    def check_all_diagonals_for_win(self):
        for y in range(6):
            diagonals = [self.get_right_up_diagonal(0, y), self.get_left_up_diagonal(6, y)]

            for diagonal in diagonals:
                if self.four_in_a_row(diagonal) != -1:
                    return self.four_in_a_row(diagonal)
        for x in range(7):
            diagonals = [self.get_left_up_diagonal(x, 0), self.get_right_up_diagonal(x, 0)]

            for diagonal in diagonals:
                if self.four_in_a_row(diagonal) != -1:
                    return self.four_in_a_row(diagonal)
        return -1

    def game_over(self):
        if self.get_free_columns() == []:
            return "exaequo"
        for column in self.columns:
            if self.four_in_a_row(column) != -1:
                return self.four_in_a_row(column)
        for y in range(6):
            row = [self.columns[x][y] for x in range(7)]
            if self.four_in_a_row(row) != -1:
                return self.four_in_a_row(row)
        if self.check_all_diagonals_for_win() != -1:
            return self.check_all_diagonals_for_win()

        return -1

    def print_grid(self):
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

    def clone(self):
        clone = Grid()
        clone.columns = [[tile for tile in column] for column in self.columns]
        return clone

    def clone_with_move(self, move, player_id):
        clone = self.clone()
        clone.add_pawn(move, player_id)
        return clone

    def get_bordering_tiles(self, xCo, yCo) -> list:
        bordering_tiles = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                if 0 <= xCo + x < self.WIDTH and 0 <= yCo + y < self.HEIGHT:
                    bordering_tiles.append(self.columns[xCo + x][yCo + y])
        return bordering_tiles

    def get_nr_moves_left(self):
        return sum([self.columns[x].count(None) for x in self.get_free_columns()])

    def get_last_move(self):
        return self.logs[-1]
