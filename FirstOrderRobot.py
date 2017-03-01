import random

OPPONENT_PLAYER_ID = 'X'

class FirstOrderRobot():
	"""This robot DOES NOT LEARN. 
	It applies simple algorithms to see if it can avoid a four in a row.
	In addition, it looks to see if the move it wants to make does create an immediate win possibility for the opponent.
	Except for that, it just plays randomly."""
	
	def findTopEmpty(self, column):
		y = 5
		while column[y] is None and y >= 0:
			y -= 1
		return y + 1 

	def hasTripletBelow(self, column, y):
		if y < 3:
			return False
		if column[y-1] == column[y-2] == column[y-3] is not None:
			return column[y-1]
		return False
			
	def hasAdjacentTriplet(self, grid, x, y):
		if x <= 3 and grid.columns[x+1][y] == grid.columns[x+2][y] == grid.columns[x+3][y] is not None:
			return grid.columns[x+1][y]
		if x >= 3 and grid.columns[x-1][y] == grid.columns[x-2][y] == grid.columns[x-3][y] is not None:
			return grid.columns[x-1][y]
		return False
	
	def hasAdjacentDoubleAndSingle(self, grid, x, y):
		if 1 <= x <= 4 and grid.columns[x-1][y] == grid.columns[x+1][y] == grid.columns[x+2][y] is not None:
			return grid.columns[x-1][y]
		if 2 <= x <= 5 and grid.columns[x-2][y] == grid.columns[x-1][y] == grid.columns[x+1][y] is not None:
			return grid.columns[x-2][y]
		return False
	
	def hasDiagonalTriplet(self, grid, x, y):
		# look up
		if y <= 2:
			# look right
			if x <= 3 and grid.columns[x+1][y+1] == grid.columns[x+2][y+2] == grid.columns[x+3][y+3] is not None:
				return grid.columns[x+1][y+1]
			# look left
			if x >= 3 and grid.columns[x-1][y+1] == grid.columns[x-2][y+2] == grid.columns[x-3][y+3] is not None:
				return grid.columns[x-1][y+1]
		if y >= 3:
			if x <= 3 and grid.columns[x+1][y-1] == grid.columns[x+2][y-2] == grid.columns[x+3][y-3] is not None:
				return grid.columns[x+1][y-1]
			if x >= 3 and grid.columns[x-1][y-1] == grid.columns[x-2][y-2] == grid.columns[x-3][y-3] is not None:
				return grid.columns[x-1][y-1]
		return False
	
	def hasDiagonalDoubleAndSingle(self, grid, x, y):
		# look up (= long tail to the right)
			# look left
		if 0 < y <= 3 and 2 <= x <= 5:
			if grid.columns[x-1][y+1] == grid.columns[x-2][y+2] == grid.columns[x+1][y-1] is not None:
				return grid.columns[x-1][y+1]
			# look right
		if 0 < y <= 3 and 1 <= x <= 4:
			if grid.columns[x-1][y+1] == grid.columns[x+1][y+1] == grid.columns[x+2][y+2] is not None:
				return grid.columns[x-1][y+1]
		#look down
			# look left
		if 2 <= y <= 4 and 2 <= x <= 5:
			if grid.columns[x-2][y-2] == grid.columns[x-1][y-1] == grid.columns[x+1][y+1] is not None:
				return  grid.columns[x-2][y-2] 
			# look right
		if 2 <= y <= 4 and 1 <= x <= 4:
			if grid.columns[x-1][y+1] == grid.columns[x+1][y-1] == grid.columns[x+2][y-2] is not None:
				return grid.columns[x-1][y+1]
		return False
	
	def checkAdjacents(self, grid, x, y):
		if self.hasAdjacentTriplet(grid, x, y):
			#print("FOUND 3-0 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return {'column':x,'player':self.hasAdjacentTriplet(grid, x, y)}
		if self.hasAdjacentDoubleAndSingle(grid, x, y):
			#print("FOUND 2-1 HORIZONTAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return {'column':x,'player':self.hasAdjacentDoubleAndSingle(grid, x, y)}
		return -1
		
	def checkDiagonals(self, grid, x, y):
		if self.hasDiagonalTriplet(grid, x, y):
			#print("FOUND 3-0 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return {'column':x,'player':self.hasDiagonalTriplet(grid, x, y)}
		if self.hasDiagonalDoubleAndSingle(grid, x, y):
			#print("FOUND 2-1 DIAGONAL THREAT AT (" + str(x) + "," + str(y) + ")")
			return {'column':x,'player':self.hasDiagonalTriplet(grid, x, y)}
		return -1
		
	def checkColumns(self, grid, freeColumns):
		for x in freeColumns:
			y= self.findTopEmpty(grid.columns[x])
			if self.hasTripletBelow(grid.columns[x], y):
				# print("FOUND VERTICAL THREAT AT (" + str(x) + "," + str(y) + ")")
				return {'column':x,'player':self.hasTripletBelow(grid.columns[x], y)}
			if self.checkAdjacents(grid, x, y) != -1:
				return self.checkAdjacents(grid, x, y)
			if self.checkDiagonals(grid, x, y) != -1:
				return self.checkDiagonals(grid, x, y)
		return -1
	
	def chooseMoveThatDoesNotHelpOpponent(self, grid):
		freeColumns = grid.getFreeColumns()
		#random.shuffle(freeColumns)
		dangerousColumns = []
		for x in freeColumns:
			y= self.findTopEmpty(grid.columns[x])
			if y == 7:
				continue
			y += 1
			if self.checkAdjacents(grid, x, y) !=-1 and self.checkAdjacents(grid, x, y) == OPPONENT_PLAYER_ID:
				print("AVOIDING TO CREATE ADJACENT TRAP AT (" + str(x) + "," + str(y) + ")")
				dangerousColumns.append(x)
				continue
			elif self.checkDiagonals(grid, x, y) !=-1 and self.checkDiagonals(grid, x, y) == OPPONENT_PLAYER_ID:
				print("AVOIDING TO CREATE DIAGONAL TRAP AT (" + str(x) + "," + str(y) + ")")
				dangerousColumns.append(x)
				continue
			# estimate if gives threat to opponent
			#else:
			#	return x
		print("DANGEROUS COLUMNS: " + str(dangerousColumns))
		return random.choice([i for i in freeColumns if i not in dangerousColumns])
		raise Exception("The robot has not found any safe moves to make!")
			
			
	def chooseMove(self, grid):
		freeColumns = grid.getFreeColumns()
		if self.checkColumns(grid, freeColumns) != -1:
			return self.checkColumns(grid, freeColumns)['column']
		else:
			return self.chooseMoveThatDoesNotHelpOpponent(grid)