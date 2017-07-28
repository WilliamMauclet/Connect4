import unittest

from Grid import Grid


class GridTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()

    def test_initialization(self):
        self.assertEqual(len(self.grid.columns), self.grid.WIDTH)
        for column in self.grid.columns:
            self.assertEqual(len(column), self.grid.HEIGHT)
        self.assertEqual(len(self.grid.logs), 0)

    def test_get_empty_top_index(self):
        for _ in range(4):
            self.grid.add_pawn(0, 'x')

        self.assertEqual(self.grid.get_empty_top_index(0), 4)

    def test_get_free_columns(self):
        for _ in range(6):
            self.grid.add_pawn(0, 'x')

        self.grid.get_free_columns()

    def test_is_full(self):
        self.assertFalse(self.grid.is_full())

        for _ in range(6):
            self.grid.add_pawn(6, 'x')

        self.assertFalse(self.grid.is_full())

        for col in range(6):
            for _ in range(6):
                self.grid.add_pawn(col, 'x')

        self.assertTrue(self.grid.is_full())

    def test_add_pawn(self):
        self.assertIsNone(self.grid.columns[4][0])
        self.assertEqual(len(self.grid.logs), 0)

        self.grid.add_pawn(4, 'x')

        self.assertIsNotNone(self.grid.columns[4][0])
        self.assertEqual(self.grid.columns[4][0], 'x')
        self.assertEqual(len(self.grid.logs), 1)

    def test_game_over_false(self):
        for col in range(0, 7, 2):
            self.grid.add_pawn(col, 'x')

        self.assertEqual(self.grid.game_over(), -1)

    def test_game_over_column(self):
        for _ in range(4):
            self.grid.add_pawn(0, 'x')

        self.assertEqual(self.grid.game_over(), 'x')

    def test_game_over_row(self):
        for col in range(2, 6):
            self.grid.add_pawn(col, 'x')

        self.assertEqual(self.grid.game_over(), 'x')

    def test_game_over_diagonal(self):
        fillers = iter(range(99))
        for col in range(4):
            for height in range(col):
                self.grid.add_pawn(col, next(fillers))
            self.grid.add_pawn(col, 'x')

        self.assertEqual(self.grid.game_over(), 'x')

    def test_game_over_exaequo(self):
        fillers = iter(range(42))
        for col in range(7):
            for _ in range(6):
                self.grid.add_pawn(col, next(fillers))

        self.assertTrue(self.grid.is_full())
        self.assertEqual(self.grid.game_over(), 'exaequo')

    def test_game_over_priorities(self):
        fillers = iter(range(42 - 7))
        for col in range(7):
            for _ in range(5):
                self.grid.add_pawn(col, next(fillers))
            self.grid.add_pawn(col, 'x')

        self.assertTrue(self.grid.is_full())
        self.assertEqual(self.grid.game_over(), 'x')

    def test_print_grid(self):
        pass

    def test_get_state_string_representation(self):
        expected = 6
        for _ in range(expected):
            self.grid.add_pawn(4, 'x')

        id_count = self.grid.get_state_string_representation().count('x')

        self.assertEqual(id_count, expected)

    def test_clone_with_move(self):
        for _ in range(4):
            self.grid.add_pawn(2, 'x')
        for _ in range(3):
            self.grid.add_pawn(5, 'y')

        clone = self.grid.clone_with_move(3, 'y')

        for height in range(4):
            self.assertEqual(self.grid.columns[2][height], 'x')
        for height in range(3):
            self.assertEqual(self.grid.columns[5][height], 'y')
        self.assertEqual(clone.columns[3][0], 'y')

    def test_clone_with_move_opponent(self):
        for _ in range(4):
            self.grid.add_pawn(2, 'x')
        for _ in range(3):
            self.grid.add_pawn(5, 'y')

        clone = self.grid.clone_with_move_opponent(3, 'y')

        for height in range(4):
            self.assertEqual(self.grid.columns[2][height], 'x')
        for height in range(3):
            self.assertEqual(self.grid.columns[5][height], 'y')
        self.assertEqual(clone.columns[3][0], 'x')

    def test_get_bordering_tiles(self):
        fillers = iter(range(99))
        for _ in range(2):
            for x in range(3):
                self.grid.add_pawn(x, next(fillers))

        bordering_tiles = list(self.grid.get_bordering_tiles(1, 1))

        self.assertCountEqual(bordering_tiles, [0, 1, 2, 3, 4, 5, None, None, None])

    def test_add_pawn_history(self):
        history = ((0, 'B'), (3, 'H'), (3, 'B'), (4, 'H'))

        self.grid.add_pawn_history(history)

        self.assertCountEqual(self.grid.logs, history)
        self.assertEqual(self.grid.columns[0][0], 'B')
        self.assertEqual(self.grid.columns[3][0], 'H')
        self.assertEqual(self.grid.columns[3][1], 'B')
        self.assertEqual(self.grid.columns[4][0], 'H')

if __name__ == '__main__':
    unittest.main()
