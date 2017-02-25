import random

class ZeroOrderRobot():
	"""This robot DOES NOT LEARN. 
	It applies simple algorithms to see if it can avoid a four in a row.
	Except for that, it just plays randomly."""
	def chooseMove(self, grid):
		freeColumns = grid.getFreeColumns()
		if checkColumns(grid, freeColumns):
			return checkColumns(grid, freeColumns)
		else:
			return random.choice(freeColumns)
		
	def checkColumns(self, grid, freeColumns):
		for x in freeColumns:
			y= findTopEmpty(grid.columns[x])
			if hasTopEmptyWithTripletBelow(grid.columns[x]):
				return x
			elif hasTopEmptyWithAdjacentTriplets(grid, x, y):
				return x
			elif hasTopEmptyWithDiagonalTriplets(grid, x, y):
				return x
		return False
	
	def findTopEmpty(self, column):
		y = 6
		while column[y] is None and y >= 0:
			y -= 1
		return y + 1 

	def hasTopEmptyWithTripletBelow(self, column, y):
		if y < 3:
			return False
		if column[y-1] is column[y-2] is column[y-3] is not None:
			return True
		else:
			return False
			
	def hasTopEmptyWithAdjacentTriplets(self, grid, x, y):
		if x <= 3 and grid.columns[x+1][y] is grid.columns[x+2][y] is grid.columns[x+3][y] is not None:
			return True
		elif x >= 3 and grid.columns[x-1][y] is grid.columns[x-2][y] is grid.columns[x-3][y] is not None:
			return True
		else:
			return False
	
	def hasTopEmptyWithDiagonalTriplets(self, grid, x, y):
		if y <= 2:
			if x <= 3 and grid.columns[x+1][y+1] is grid.columns[x+2][y+2] is grid.columns[x+3][y+3] is not None:
				return True
			elif x >= 3 and grid.columns[x-1][y+1] is grid.columns[x-2][y+1] is grid.columns[x-3][y+1] is not None:
				return True
		elif y >= 3:
			if x <= 3 and grid.columns[x+1][y-1] is grid.columns[x+2][y-2] is grid.columns[x+3][y-3] is not None:
				return True
			elif x >= 3 and grid.columns[x-1][y-1] is grid.columns[x-2][y-2] is grid.columns[x-3][y-3] is not None:
				return True
		else:
			return False
	