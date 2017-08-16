import unittest
import ast
from Grid import Grid
from MinmaxBot import MinmaxBot


class MinmaxBotTest(unittest.TestCase):
    def setUp(self):
        self.minmaxBot = MinmaxBot('B')
        self.grid = Grid()

    def test_replay_1(self):
        with open("/home/wmclt/Projects/Connect4/Hispida/docs/replays/minmaxBot_1.txt", "r") as reader:
            # ast.literal_eval converts string representations into actual instances
            # https://stackoverflow.com/a/1894296
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertEqual(self.minmaxBot.choose_move(self.grid), 3)

    def test_replay_2(self):
        with open("/home/wmclt/Projects/Connect4/Hispida/docs/replays/minmaxBot_2.txt", "r") as reader:
            # ast.literal_eval converts string representations into actual instances
            # https://stackoverflow.com/a/1894296
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)

            self.assertIn(self.minmaxBot.choose_move(self.grid), [2, 5])

