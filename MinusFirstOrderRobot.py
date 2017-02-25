import random

class MinusFirstOrderRobot():
	def chooseMove(self, grid):
		return random.choice(grid.getFreeColumns())