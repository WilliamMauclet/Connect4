class ColumnGrid:
	def __init__(self):
		self.columns = [ [None for i in range(0,6)] for j in range(0,7)] 
		
	def getColumn(self, x):
		return self.columns[x]
	
	def getFreeColumns(self):
		return [ x for x in range(0,7) if self.isColumnFree(x)]
	
	def isColumnFree(self, x):
		return self.columns[x][-1] is None
	
	def addPawn(self, x, playerId):
		for y in range(0,6):
			if self.columns[x][y] is None:
				self.columns[x][y] = playerId
				return
		assert False, "Column " + str(x) + " was already full." + getGrid
	
	def checkConsistency(self):
		#assert len(self.columns) is 7, str(len(self.columbs) + " many columns found O.o"
		#nrPawnsDict = {None:0,PLAYER_ID_1:0,PLAYER_ID_2:0}
		for column in self.columns:
			assert len(column) is 6, "Column " + str(column) + " has " + len(column) + " tiles! " + str(column) 
		#	for tile in column:
		#		nrPawnsDict[tile] += nrPawnsDict[tile]
		#assert nrPawnsDict 
	
	def fourInARow(self, row):
		seq = 1
		prev = None
		for tile in row:
			if tile is None or tile != prev:
				seq = 1
			elif tile == prev:
				seq += 1
			
			if seq is 4:
				return tile
			prev = tile
		return -1
	
	def getRightUpDiagonal(self, x, y):
		row = []
		while x < 6 and y < 5:
			row.append(self.columns[x][y])
			x += 1
			y += 1
		return row
	
	def getLeftUpDiagonal(self, x, y):
		row = []
		while x > 0 and y < 5:
			row.append(self.columns[x][y])
			x -= 1
			y += 1
		return row
	
	def checkAllDiagonalsForWin(self):
		for i in range(0,6):
			diagonals = [self.getRightUpDiagonal(0,i), self.getLeftUpDiagonal(6,i)]
			
			for diagonal in diagonals:
				if self.fourInARow(diagonal) != -1:
					return self.fourInARow(diagonal)
		for i in range(0,7):
			diagonals = [self.getLeftUpDiagonal(i,0), self.getRightUpDiagonal(i,0)]
			
			for diagonal in diagonals:
				if self.fourInARow(diagonal) != -1:
					return self.fourInARow(diagonal)
		return -1
	
	def gameOver(self):
		for column in self.columns:
			if self.fourInARow(column):
				return self.fourInARow(column)
		for y in range(0,6):
			row = [self.columns[x][y] for x in range(0,7)]
			if self.fourInARow(row):
				return self.fourInARow(row)
		
		if self.checkAllDiagonalsForWin() != -1:
			return self.checkAllDiagonalsForWin()
			
		return -1
	
	def printGrid(self):
		image = ''
		for x in range(0,15):
			image += '_'
		for y in range(5,-1,-1):
			image += '\n|' 
			for x in range(0,7):
				if self.columns[x][y] is None:
					image += '_|'
				else:
					image += self.columns[x][y] + '|'
		image += '\n'
		for x in range(0,15):
			image += "-"
		print(image)
		
	
	