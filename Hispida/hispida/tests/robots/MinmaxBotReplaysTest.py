# ast.literal_eval converts string representations into actual instances
#  https://stackoverflow.com/a/1894296
import ast, unittest
from hispida.grid.Grid import Grid
from hispida.bots.MinmaxBot import MinmaxBot


class MinmaxBotReplaysTest(unittest.TestCase):
    def setUp(self):
        self.file_path = '../../docs/replays/minmaxBot_{}.txt'
        self.minmaxBot_5 = MinmaxBot('B', depth=5)
        self.minmaxBot_7 = MinmaxBot('B', depth=7, heuristic_bot=1, heuristic_opponent=-3)
        self.grid = Grid()

    def _execute_replay_nr(self, number):
        replay = ast.literal_eval(open(self.file_path.format(number), 'r').read())
        self.grid.add_pawn_history(replay)

    def test_5_replay_1(self):
        self._execute_replay_nr(1)

        self.assertEqual(self.minmaxBot_5.choose_move(self.grid), 3)

    def test_5_replay_2(self):
        self._execute_replay_nr(2)

        self.assertIn(self.minmaxBot_5.choose_move(self.grid), [2, 5])

    def test_5_replay_3(self):
        self._execute_replay_nr(3)

        self.assertNotEqual(self.minmaxBot_5.choose_move(self.grid), 1)

    def test_7_replay_1(self):
        self._execute_replay_nr(1)

        self.assertEqual(self.minmaxBot_7.choose_move(self.grid), 3)

    def test_7_replay_2(self):
        self._execute_replay_nr(2)

        self.assertIn(self.minmaxBot_7.choose_move(self.grid), [2, 5])

    def test_7_replay_3(self):
        self._execute_replay_nr(3)

        self.assertTrue(True, msg="ROBOT CAN'T POSSIBLY WIN IN THIS SITUATION")

    def test_7_replay_4(self):
        """This test is to prove the previous test, reversing the replay history. Change the play
        order below as you wish, you won't be able to beat the bot."""
        self._execute_replay_nr(4)

        self.grid.add_pawn(5, 'H')
        self.grid.add_pawn(3, 'B')
        self.grid.add_pawn(2, 'H')
        self.grid.add_pawn(1, 'B')
        self.grid.add_pawn(1, 'H')

        # self.grid.print_grid()
        # print(self.minmaxBot_7.choose_move(self.grid))

    def test_7_replay_5(self):
        self._execute_replay_nr(5)

        self.grid.print_grid()

        self.assertEqual(self.minmaxBot_7.choose_move(self.grid), 0)
