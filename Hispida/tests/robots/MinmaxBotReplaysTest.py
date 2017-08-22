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

            self.assertTrue(True, msg="ROBOT CAN'T POSSIBLY WIN IN THIS SITUATION")

    def test_7_replay_4(self):
        """This test is to prove the previous test, reversing the replay history. Change the play
        order below as you wish, you won't be able to beat the bot."""
        with open(self.file_path.format(4), "r") as reader:
            replay = ast.literal_eval(reader.read())
            self.grid.add_pawn_history(replay)
            self.grid.add_pawn(5, 'H')
            self.grid.add_pawn(3, 'B')
            self.grid.add_pawn(2, 'H')
            self.grid.add_pawn(1, 'B')
            self.grid.add_pawn(1, 'H')

            self.grid.print_grid()

            print(self.minmaxBot_7.choose_move(self.grid))

    def test_whatever(self):
        print(self.minmaxBot_5.get_configuration())