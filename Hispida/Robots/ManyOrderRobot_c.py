import random

from Robots.FirstOrderRobot import FirstOrderRobot


class ManyOrderRobot_C(FirstOrderRobot):
    """It applies simple algorithms to see if it can avoid a four in a row.
    In addition, it looks to see if the move it wants to make does create a future win possibility for the opponent.
    Except for that, it just plays randomly."""

    WIN_SCORE = 20
    LOSE_SCORE = -1
    EXAEQUO_SCORE = 0
    # only 2n+1 iterations considered
    # 3 should be just as good as FirstOrderRobot
    # should only work for values 2n+1
    LOOK_AHEADS = 5

    def apply_leaf_heuristic(self, grid, xCo, yCo):
        heuristic_score = 0
        for tile in grid.get_bordering_tiles(xCo, yCo):
            if tile == self.robotId:
                heuristic_score += 2
            elif tile == self.get_id_opponent():
                heuristic_score += 1
        return heuristic_score

    def evaluate_leaf_move(self, grid, x):
        height = 'placeholder'
        for y in range(6):
            if grid.columns[x][y] is None:
                height = y
        new_grid = grid.clone_with_move(x, self.robotId)
        if new_grid.game_over() == self.robotId:
            return 20
        else:
            return self.apply_leaf_heuristic(new_grid, x, height)

    def leaf_iteration(self, grid):
        """Tail of the recursion. Should return a dictionary with keys from 0 to 6 and a score for each.
        If victory possible for player: +1, if not: 0. In negative if opponent."""
        moves_scores = []
        for move in grid.get_free_columns():
            moves_scores.append(self.evaluate_leaf_move(grid, move))

        return max(moves_scores)

    def max_iteration(self, grid, look_aheads_left) -> int:
        moves_scores = []

        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robotId)
            if new_grid.game_over() == self.robotId:
                return self.WIN_SCORE
            elif new_grid.game_over() == 'exaequo':
                moves_scores.append(self.EXAEQUO_SCORE)
            else:
                moves_scores.append(self.min_iteration(new_grid, look_aheads_left - 1))

        return max(moves_scores)

    def min_iteration(self, grid, look_aheads_left) -> int:
        moves_scores = []
        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.get_id_opponent())
            if new_grid.game_over() == self.get_id_opponent():
                return self.LOSE_SCORE
            elif new_grid.game_over() == 'exaequo':
                moves_scores.append(self.EXAEQUO_SCORE)
            elif look_aheads_left == 2:
                moves_scores.append(self.leaf_iteration(new_grid))
            else:
                moves_scores.append(self.max_iteration(new_grid, look_aheads_left - 1))

        return min(moves_scores)

    def choose_move_with_minmax(self, grid) -> int:
        #TODO like max iteration except must remember move
        moves_scores = []

        for x in grid.get_free_columns():
            new_grid = grid.clone_with_move(x, self.robotId)
            #if new_grid.game_over(): -> IMPOSSIBLE
            #    return x
            #else:
            if len(new_grid.get_free_columns()) == 0: # TODO because check_if_immediate_win_possible does not check on exaequo! OR DOES IT??? TODO
                moves_scores.append({'move':x, 'score':0})
            else:
                moves_scores.append({'move':x,'score':self.min_iteration(new_grid, self.LOOK_AHEADS -1)})

        return max(moves_scores, key=lambda move: move['score'])['move']
        # TODO replaced by one-liner above
        #max_score = max([move['score'] for move in moves_scores])
        #for move in moves_scores:
        #    if move['score'] == max_score:
        #        return move['move']

    def choose_move(self, grid):
        if self.check_if_immediate_win_possible(grid):
            return self.check_if_immediate_win_possible(grid)['column']
        else:
            return self.choose_move_with_minmax(grid)
