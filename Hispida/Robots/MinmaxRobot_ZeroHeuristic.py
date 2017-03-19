from Robots.MinmaxRobot import MinmaxRobot


class MinmaxRobot_ZeroHeuristic(MinmaxRobot):
    """Heuristic: no heuristic."""

    def apply_leaf_heuristic(self, grid, xCo, yCo) -> int:
        return 0