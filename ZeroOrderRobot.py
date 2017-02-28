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
		if column[y-1] == column[y-2] == column[y-3] is not None:
			return True
		return False
			
	def hasTopEmptyWithAdjacentTriplets(self, grid, x, y):
		if x <= 3 and grid.columns[x+1][y] == grid.columns[x+2][y] == grid.columns[x+3][y] is not None:
			return True
		if x >= 3 and grid.columns[x-1][y] == grid.columns[x-2][y] == grid.columns[x-3][y] is not None:
			return True
		return False
	
	def hasTopEmptyWithAdjacentDoubleAndSingle(self, grid, x, y):
		if 1 <= x <= 4 and grid.columns[x-1][y] == grid.columns[x+1][y] == grid.columns[x+2][y] is not None:
			return True
		if 2 <= x <= 5 and grid.columns[x-2][y] == grid.columns[x-1][y] == grid.columns[x+1][y] is not None:
			return True
		return False
	
	def hasTopEmptyWithDiagonalTriplets(self, grid, x, y):
		# look up
		if y <= 2:
			# look right
			if x <= 3 and grid.columns[x+1][y+1] == grid.columns[x+2][y+2] == grid.columns[x+3][y+3] is not None:
				return True
			# look left
			if x >= 3 and grid.columns[x-1][y+1] == grid.columns[x-2][y+2] == grid.columns[x-3][y+3] is not None:
				return True
		if y >= 3:
			if x <= 3 and grid.columns[x+1][y-1] == grid.columns[x+2][y-2] == grid.columns[x+3][y-3] is not None:
				return True
			if x >= 3 and grid.columns[x-1][y-1] == grid.columns[x-2][y-2] == grid.columns[x-3][y-3] is not None:
				return True
		return False
	
	def hasTopEmptyWithDiagonalDoubleAndSingle(self, grid, x, y):
		# look up (= long tail to the right)
			# look left
		if 0 < y <= 3 and 2 <= x <= 5:
			if grid.columns[x-1][y+1] == grid.columns[x-2][y+2] == grid.columns[x+1][y-1] is not None:
				return True
			# look right
		if 0 < y <= 3 and 1 <= x <= 4:
			if grid.columns[x-1][y+1] == grid.columns[x+1][y+1] == grid.columns[x+2][y+2] is not None:
				return True
		#look down
			# look left
		if 2 <= y <= 4 and 2 <= x <= 5:
			if grid.columns[x-2][y-2] == grid.columns[x-1][y-1] == grid.columns[x+1][y+1] is not None:
				return True
			# look right
		if 2 <= y <= 4 and 1 <= x <= 4:
			if grid.columns[x-1][y+1] == grid.columns[x+1][y-1] == grid.columns[x+2][y-2] is not None:
				return True
		return False
	
	def checkAdjacents(self, grid, x, y):
		if self.hasTopEmptyWithAdjacentTriplets(grid, x, y):
			print("FOUND 3-0 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return x
		if self.hasTopEmptyWithAdjacentDoubleAndSingle(grid, x, y):
			print("FOUND 2-1 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return x
		return -1
		
	def checkDiagonals(self, grid, x, y):
		if self.hasTopEmptyWithDiagonalTriplets(grid, x, y):
			print("FOUND 3-0 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return x
		if self.hasTopEmptyWithDiagonalDoubleAndSingle(grid, x, y):
			print("FOUND 2-1 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return x
		return -1
		
	def checkColumns(self, grid, freeColumns):
		for x in freeColumns:
			y= self.findTopEmpty(grid.columns[x])
			if self.hasTopEmptyWithTripletBelow(grid.columns[x], y):
				print("FOUND VERTICAL THREAT AT (" + str(x) + "," + str(y) + ")")
				return x
			if self.checkAdjacents(grid, x, y) != -1:
				return self.checkAdjacents(grid, x, y)
			if self.checkDiagonals(grid, x, y) != -1:
				return self.checkDiagonals(grid, x, y)
		return -1
	
	def chooseMove(self, grid):
		freeColumns = grid.getFreeColumns()
		if self.checkColumns(grid, freeColumns) != -1:
			return self.checkColumns(grid, freeColumns)
		else:
			return random.choice(freeColumns)
