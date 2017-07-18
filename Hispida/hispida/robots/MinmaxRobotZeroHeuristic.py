from hispida.robots import MinmaxRobot


class MinmaxRobotZeroHeuristic(MinmaxRobot):
    """Heuristic: no heuristic."""

    def apply_leaf_heuristic(self, grid) -> int:
        return 0

    def get_configuration(self) -> dict:
        return {
            "WIN_SCORE": self.WIN_SCORE,
            "LOSE_SCORE": self.LOSE_SCORE,
            "EXAEQUO_SCORE": self.EXAEQUO_SCORE,
            "DEPTH": self.DEPTH
        }
