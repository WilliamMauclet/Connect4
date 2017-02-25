import random

class ZeroOrderRobot():
	"""This robot DOES NOT LEARN. 
	It applies simple algorithms to see if it can avoid a four in a row.
	Except for that, it just plays randomly."""		
	def findTopEmpty(self, column):
		y = 5
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
		
	def checkColumns(self, grid, freeColumns):
		for x in freeColumns:
			y= self.findTopEmpty(grid.columns[x])
			if self.hasTopEmptyWithTripletBelow(grid.columns[x], y):
				print("FOUND VERTICAL THREAT IN COLUMN " + str(x))
				return x
			elif self.hasTopEmptyWithAdjacentTriplets(grid, x, y):
				print("FOUND HORIZONTAL THREAT IN COLUMN " + str(x))
				return x
			elif self.hasTopEmptyWithDiagonalTriplets(grid, x, y):
				print("FOUND DIAGONAL THREAT IN COLUMN " + str(x))
				return x
		return -1
		
	def chooseMove(self, grid):
		freeColumns = grid.getFreeColumns()
		if not self.checkColumns(grid, freeColumns) == -1:
			return self.checkColumns(grid, freeColumns)
		else:
			return random.choice(freeColumns)
	