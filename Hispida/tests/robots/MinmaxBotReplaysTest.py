import unittest
# ast.literal_eval converts string representations into actual instances
#  https://stackoverflow.com/a/1894296
import ast
from Grid import Grid
from MinmaxBot import MinmaxBot


class MinmaxBotReplaysTest(unittest.TestCase):
    def setUp(self):
        self.file_path = '/home/wmclt/Projects/Connect4/Hispida/docs/replays/minmaxBot_{}.txt'
        self.minmaxBot_5 = MinmaxBot('B', depth=5)
        self.minmaxBot_7 = MinmaxBot('B', heuristic_opponent=0, heuristic_bot=0, depth=7)
        self.grid = Grid()

    def test_5_replay_1(self):
        with open(self.file_path.format(1), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertEqual(self.minmaxBot_5.choose_move(self.grid), 3)

    def test_5_replay_2(self):
        with open(self.file_path.format(2), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertIn(self.minmaxBot_5.choose_move(self.grid), [2, 5])

    def test_5_replay_3(self):
        with open(self.file_path.format(3), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertNotEqual(self.minmaxBot_5.choose_move(self.grid), 1)

    def test_7_replay_1(self):
        with open(self.file_path.format(1), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertEqual(self.minmaxBot_7.choose_move(self.grid), 3)

    def test_7_replay_2(self):
        with open(self.file_path.format(2), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertIn(self.minmaxBot_7.choose_move(self.grid), [2, 5])

    def test_7_replay_3(self):
        with open(self.file_path.format(3), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.grid.print_grid()

            # ROBOT CAN'T POSSIBLY WIN
            self.assertNotEqual(self.minmaxBot_7.choose_move(self.grid), 1)
