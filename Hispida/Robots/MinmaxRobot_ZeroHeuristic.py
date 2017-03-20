from Robots.MinmaxRobot import MinmaxRobot


class MinmaxRobot_ZeroHeuristic(MinmaxRobot):
    """Heuristic: no heuristic."""

    def apply_leaf_heuristic(self, grid, xCo, yCo) -> int:
        return 0

    def get_advanced_description(self):
        return "WIN_SCORE=" + str(self.WIN_SCORE) + \
               "/LOSE_SCORE=" + str(self.LOSE_SCORE) + \
               "/EXAEQUO_SCORE=" + str(self.EXAEQUO_SCORE) + \
               "/LOOK_AHEADS=" + str(self.LOOK_AHEADS)