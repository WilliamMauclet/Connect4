class SmartRobot():
	def chooseMove(self, grid):
		raise NotImplementedError("Should return an 0 <= column <= 6")
		
	def checkColumns(self, grid):
		for column in grid.columns:
			if checkIfThreeSameTopPawns(column):
				return column
	
	def checkIfThreeSameTopPawns(self, column):
		seq = 0
		prev = None
		for tile in column[::-1]:
			if tile is None:
				seq = 1
			elif tile is prev:
				seq +=1
			prev = tile
		
			if seq is 3:
				return tile
				
		return False
	
	def checkRowsFirstDegree(self, grid):
		raise NotImplementedError("Should check if any row has 3 same pawns, with one empty tile above a filled tile at either side")
		
		
	