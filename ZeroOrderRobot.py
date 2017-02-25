import random

class ZeroOrderRobot():
	def chooseMove(self, grid):
		freeColumns = grid.getFreeColumns()
		if checkColumns(grid, freeColumns):
			return checkColumns(grid, freeColumns)
		else:
			return random.choice(freeColumns)
		
	def checkColumns(self, grid, freeColumns):
		for column in grid.columns:
			if hasTopEmptyWithTripletBelow(column):
				return column
			elif hasTopEmptyWithAdjacentTriplets(column):
				return column
			elif hasTopEmptyWithDiagonalTriplets(column):
				return column
		return False
	
	def findTopEmpty(self, column):
		y = 6
		while column[y] is None and y >= 0:
			y -= 1
		return y + 1 

	def hasTopEmptyWithTripletBelow(self, column):
		y = findTopEmpty(column)
		
		if y < 3:
			return False
		
		seq = 0
		prev = column[y]
		y -= 1
		while column[y] is prev:
			seq +=1
		if seq is 3:
			return True
		else:	
			return False
			
	def hasTopEmptyWithAdjacentTriplets(self, grid, x):
		y = findTopEmpty(column)
		if x <= 3 and grid.columns[x+1][y] is grid.columns[x+2][y] is grid.columns[x+3][y] is not None:
			return True
		elif x >= 3 and grid.columns[x-1][y] is grid.columns[x-2][y] is grid.columns[x-3][y] is not None:
			return True
		else:
			return False
	
	def hasTopEmptyWithDiagonalTriplets(self, grid, x):
		y = findTopEmpty(grid.columns[x])
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
	