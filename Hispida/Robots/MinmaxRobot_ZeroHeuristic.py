from Robots.MinmaxRobot import MinmaxRobot


class MinmaxRobot_ZeroHeuristic(MinmaxRobot):
    """Heuristic: no heuristic."""

    def apply_leaf_heuristic(self, grid, xCo, yCo) -> int:
        return 0

    def get_configuration(self):
        return {
            "WIN_SCORE": self.WIN_SCORE,
            "LOSE_SCORE": self.LOSE_SCORE,
            "EXAEQUO_SCORE": self.EXAEQUO_SCORE,
            "LOOK_AHEADS": self.LOOK_AHEADS
        }
